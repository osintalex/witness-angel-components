import socket
from datetime import datetime
from pathlib import Path

import importlib
import os
import sys

APP_IS_FROZEN = getattr(sys, "frozen", False)

SERVICE_MARKER_CLI_PARAM = "--service"


def _is_service_alive():

    from kivy.utils import platform
    from wacomponents.service_control import get_osc_client

    osc_client = get_osc_client(to_app=False)

    sock = osc_client.sock
    if platform != "win" and sock.family == getattr(socket, "AF_UNIX", None):
        # Trouble is on Unix systems only, with autodeleted unix socket files

        address = osc_client.address

        try:
            sock.connect(address)

            return True
        except (ConnectionRefusedError, FileNotFoundError):
            pass

    return False


def launch_main_module_with_crash_handler(main_module: str, client_type: str):
    """
    Launcher used both for main app or service, depending on parameters, and
    uplaod a crash report if an abormal exception occurs on mobile platform.
    """

    assert client_type in ("SERVICE", "APPLICATION"), client_type

    from wacomponents.application import setup_app_environment

    setup_app_environment(setup_kivy_gui=(client_type == "APPLICATION"))

    # We can only do it now that Kivy is setup!
    if client_type == "SERVICE":
        sys.modules["kivymd.uix"] = None  # Force early failure if service tries to load Kivy GUI
        if _is_service_alive():
            dt = datetime.now()
            print(">>> %s - Witness Angel Recorder service already started and listening on its UNIX socket, aborting relaunch" % dt)
            return

    try:
        module = importlib.import_module(main_module)  # NOW ONLY we trigger conf loading
        module.main()
    except Exception:
        if "ANDROID_ARGUMENT" not in os.environ:  # FIXME setup IOS crash handler too
            raise  # Desktop should not be impacted by crash handler
        print(">>> FATAL ERROR IN %s LAUNCHER ON MOBILE PLATFORM, SENDING CRASH REPORT <<" % client_type)
        exc_info = sys.exc_info()
        target_url = (
            "https://api.witnessangel.com/support/crashdumps/"
        )  # HARDCODED - Can't access common config safely here
        from wacomponents.logging.crashdumps import generate_and_send_crashdump  # Should be mostly safe to import

        report = generate_and_send_crashdump(exc_info=exc_info, target_url=target_url, client_type=client_type)
        print(report)  # Not sent to stderr for now, since it is hooked by Kivy logging
        raise


def launch_app_or_resurrect_service_with_crash_handler(app_module, service_module, main_file, sys_argv):
    if SERVICE_MARKER_CLI_PARAM in sys_argv:

        launch_main_module_with_crash_handler(main_module=service_module, client_type="SERVICE")

    else:

        if not os.getenv("WA_SERVICE_SCRIPT"):
            if APP_IS_FROZEN:
                wa_service_script = SERVICE_MARKER_CLI_PARAM  # sys.executable is sufficient for script itself
            else:
                wa_service_script = str(Path(main_file).resolve()) + "|" + SERVICE_MARKER_CLI_PARAM
            os.environ["WA_SERVICE_SCRIPT"] = wa_service_script

        launch_main_module_with_crash_handler(main_module=app_module, client_type="APPLICATION")
