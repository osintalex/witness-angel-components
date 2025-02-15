import logging
from configparser import ConfigParser, Error as ConfigParserError

import os
from oscpy.server import ServerClass

from wacomponents.application._common_runtime_support import WaRuntimeSupportMixin
from wacomponents.default_settings import IS_ANDROID, WIP_RECORDING_MARKER
from wacomponents.logging.handlers import safe_catch_unhandled_exception
from wacomponents.recording_toolchain import start_recording_toolchain, stop_recording_toolchain
from wacomponents.service_control import get_osc_server, get_osc_client
from wacomponents.utilities import InterruptableEvent, MONOTHREAD_POOL_EXECUTOR

# os.environ["KIVY_NO_CONSOLELOG"] = "1"  # IMPORTANT

osc, osc_starter_callback = get_osc_server(is_application=False)

# FIXME what happens if exception on remote OSC endpoint ? CRASH!!
# TODO add custom "local trustee resolver"
# TODO add exception swallowers


logger = logging.getLogger(__name__)


if IS_ANDROID:
    from wacomponents.application.android_helpers import preload_java_classes

    preload_java_classes()


class ActivityNotificationType:
    RECORDING_PROGRESS = "RECORDING_PROGRESS"  # Sent with "notification_color" argument
    IMAGE_PREVIEW = "IMAGE_PREVIEW"  # Sent with "notification_image" arguments


@ServerClass
class WaRecorderService(WaRuntimeSupportMixin):
    """
    The background server automatically starts when service script is launched.

    It must be stopped gracefully with a call to "/stop_server", so that current recordings can be properly stored.

    While the server is alive, recordings can be started and stopped several times without problem.
    """

    _sock = None
    _recording_toolchain = None
    _status_change_in_progress = False  # Set to True while recording is starting/stopping

    def __init__(self):

        logger.info("Service is starting")  # Will not be sent to App (too early)
        osc_starter_callback()  # Opens server port
        self._osc_client = get_osc_client(to_app=True)

        # Redirect root logger traffic to GUI console widget if wanted
        # logging.getLogger(None).addHandler(CallbackLoggingHandler(self._remote_logging_callback))

        self._termination_event = InterruptableEvent()
        logger.info("Service is started")

        self.reload_config()

        # Initial setup of service according to persisted config
        try:
            daemonize_service = self.config.getboolean(
                "usersettings", "daemonize_service"
            )  # FIXME is that really "usersettings" here?
        except ConfigParserError:
            daemonize_service = False  # Probably App is just initializing itself
        self.switch_daemonize_service(daemonize_service)

        # import traceback; traceback.print_stack()

    def _get_cryptoconf(self):
        """Return a wacryptolib-compatible encryption configuration"""
        raise NotImplementedError("_get_cryptoconf()")

    def _build_recording_toolchain(self):
        """Return a valid recording toolchain"""
        raise NotImplementedError("_build_recording_toolchain()")

    def reload_config(self, filename=None):  # FIXME move to generic app ?

        # FIXME always parse default values too, in case service gets restarted alone after upgrade of python packages??

        if not filename:
            filename = self.config_file_path

        logger.info(f"Service reloading config file {filename}")

        # No NAME here, since named parsers must be Singletons in process!
        config = ConfigParser()
        config.read(str(self.config_defaults_path))  # Default values

        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(filename)
            config.read(str(filename))  # Actually fails silently if file not found
        except (ConfigParserError, FileNotFoundError) as exc:
            logger.error(f"Service ignored missing or corrupted config file {filename} ({exc!r})")

        # logger.info(f"Config file {filename} loaded")
        self.config = config

    def __DISABLED_remote_logging_callback(self, msg):
        max_length = 64000  # Beware OSCP server expects max 65535 in input, prevent overflow here
        if len(msg) > max_length:
            msg = msg[:max_length] + "<truncated...>"
        return self._send_message("/log_output", "Service: " + msg)

    def _send_message(self, address, *values):
        logger.debug("Message sent from service to app: %s %s", address, values)
        try:
            return self._osc_client.send_message(address, values=values, safer=True)
        except OSError as exc:
            ##print("FATAL eror when sending OSC message: %r\n" % exc)
            ## NO PRINT/LOGGING HERE, in case logs get forwarded via OSC too...
            ##print("{SERVICE} Could not send osc message %s%s to app: %r"
            ##       % (address, values, exc))
            return

    def _offload_task(self, method, *args, **kwargs):  # FIXME move to common runtime
        return MONOTHREAD_POOL_EXECUTOR.submit(method, *args, **kwargs)

    @osc.address_method("/ping")
    @safe_catch_unhandled_exception
    def ping(self):
        logger.info("Ping successful!")
        self._send_message("/log_output", "Pong")

    @safe_catch_unhandled_exception
    def _offloaded_switch_daemonize_service(self, value):
        value = bool(value)  # Normalize from possible integer
        logger.info("Switching background service persistence to %s", value)
        if IS_ANDROID:
            from jnius import autoclass

            PythonService = autoclass("org.kivy.android.PythonService")
            PythonService.mService.setAutoStopService(not value)
        # Nothing to do for desktop platforms

    @osc.address_method("/switch_daemonize_service")
    @safe_catch_unhandled_exception
    def switch_daemonize_service(self, value):
        return self._offload_task(self._offloaded_switch_daemonize_service, value=value)

    @safe_catch_unhandled_exception
    def _offloaded_start_recording(self, env):
        try:
            if self.is_recording:
                # logger.debug("Ignoring redundant call to service.start_recording()")
                return
            logger.info("Service offloaded-starting recording")

            if not self._recording_toolchain:
                self._recording_toolchain = (
                    self._build_recording_toolchain()
                )  # FIXME handle exceptions instead of None!

            assert self._recording_toolchain
            start_recording_toolchain(self._recording_toolchain)
            logger.info("Service successfully offloaded-started recording")

            if IS_ANDROID:
                from wacomponents.default_settings import ANDROID_CONTEXT
                from wacomponents.application.android_helpers import build_notification_channel, build_notification

                build_notification_channel(ANDROID_CONTEXT, "Witness Angel Service")
                notification = build_notification(
                    ANDROID_CONTEXT,
                    title="Sensors are active",
                    message="Click to manage Witness Angel state",
                    ticker="Witness Angel sensors are active",
                )
                notification_uid = 1
                ANDROID_CONTEXT.startForeground(notification_uid, notification)

        except Exception as exc:
            logger.error("Could not build recording toolchain: %r", exc, exc_info=True)
        finally:
            self._status_change_in_progress = False
            self.broadcast_recording_state()  # Even on error

    @osc.address_method("/start_recording")
    @safe_catch_unhandled_exception
    def start_recording(self, env=None):
        # Fixme - remove "env" parameter if unused?
        if self._status_change_in_progress:
            logger.info("Service recording start ignored, because other status change is already in progress")
            return
        logger.info("Service got command to START the recording")

        WIP_RECORDING_MARKER.touch(exist_ok=True)
        self.reload_config()  # Important
        status, messages = self.refresh_checkup_status()
        if not status:
            logger.error("Service failed to start recording because of configuration issues: %s", "; ".join(messages))
            return

        self._status_change_in_progress = True  # We do it LAST MINUTE!
        return self._offload_task(self._offloaded_start_recording, env=env)

    @property
    def is_recording(self):
        return bool(self._recording_toolchain and self._recording_toolchain["sensors_manager"].is_running)

    @osc.address_method("/broadcast_recording_state")
    @safe_catch_unhandled_exception
    def broadcast_recording_state(self):
        """
        Broadcasts a TERNARY state, with the special value "" if a status change is in progress
        (since OSC doesn't like None values...)
        """
        if self._status_change_in_progress:
            is_recording = ""  # For ternary value, since None is not supported by OSC
        else:
            is_recording = self.is_recording
        logger.debug("Broadcasting service state is_recording=%r", is_recording)
        self._send_message("/receive_recording_state", is_recording)

    @safe_catch_unhandled_exception
    def _offloaded_stop_recording(self):
        try:
            if not self.is_recording:
                # logger.debug("Ignoring redundant call to service.stop_recording()")
                return
            logger.info("Service offloaded-stopping recording")
            stop_recording_toolchain(self._recording_toolchain)
            logger.info("Service successfully offloaded-stopped recording")

            if IS_ANDROID:
                from wacomponents.default_settings import ANDROID_CONTEXT

                ANDROID_CONTEXT.stopForeground(True)  # Does remove notification

        finally:  # Trigger all this even if container flushing failed
            self._recording_toolchain = None  # Will force a reload of config on next recording
            self._status_change_in_progress = False
            self.broadcast_recording_state()

    @osc.address_method("/stop_recording")
    @safe_catch_unhandled_exception
    def stop_recording(self, force=False):
        # print("@@ IMPORTANT - RECEIVED ORDER TO STOP RECORDING IN SERVICE")
        if self._status_change_in_progress and not force:
            logger.info("Service recording stop ignored, because other status change is already in progress")
            return
        logger.info("Service got command to STOP the recording")
        try:
            WIP_RECORDING_MARKER.unlink()  # TODO use "missing_ok" asap
        except FileNotFoundError:
            pass
        self._status_change_in_progress = True  # Do it last minute!
        return self._offload_task(self._offloaded_stop_recording)

    @osc.address_method("/stop_server")
    @safe_catch_unhandled_exception
    def stop_server(self):
        logger.info("Service got command to SHUTDOWN entirely")

        if self.is_recording:
            logger.info("Recording is currently in progress, we stop it as part of service shutdown")
            future = self.stop_recording(force=True)  # Could be None if unexpected exception was caught!
            if future:
                future.result(timeout=30)  # SYNCHRONOUS CALL (but through threadpool still)

        osc.stop_all()
        self._termination_event.set()
        logger.info("Service shutdown is now complete")

    @safe_catch_unhandled_exception
    def join(self):
        """
        Wait for the termination of the background server
        (meant for use by the main thread of the service process).
        """
        self._termination_event.wait()
