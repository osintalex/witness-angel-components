import logging
from pathlib import Path

from functools import partial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty

from wacomponents.i18n import tr
from wacomponents.screens.base import WAScreenName, WAScreenBase
from wacomponents.utilities import LINEBREAK, MONOTHREAD_POOL_EXECUTOR
from wacomponents.widgets.popups import (
    dialog_with_close_button,
    process_method_with_gui_spinner,
    help_text_popup,
    safe_catch_unhandled_exception_and_display_popup,
)
from wacryptolib.authenticator import initialize_authenticator
from wacryptolib.keygen import generate_keypair
from wacryptolib.keystore import FilesystemKeystore
from wacryptolib.utilities import generate_uuid0, catch_and_log_exception

Builder.load_file(str(Path(__file__).parent / "authenticator_creation_form.kv"))


logger = logging.getLogger(__name__)


GENERATED_KEYS_COUNT = 3  # Not too high, since mobile devices have trouble with that!
PASSPHRASE_MIN_LENGTH = 20
MAX_WA_CHARFIELD_LENGTH = 100


class AuthenticatorCreationFormScreen(WAScreenBase):

    selected_authenticator_dir = ObjectProperty(None, allownone=True)

    operation_status = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def go_to_home_screen(self):
        self.manager.current = WAScreenName.authenticator_management

    def reset_initialization_form(self):
        self.set_form_fields_status(enabled=True)
        self.ids.button_initialize.disabled = False
        self.operation_status = ""
        self._do_update_progress_bar(0)
        self.ids.initialization_form_toolbar.disabled = False

    def get_form_values(self):
        return dict(
            keystore_owner=self.ids.formfield_username.text.strip(),
            keystore_passphrase=self.ids.formfield_passphrase.text.strip(),
            keystore_passphrase_hint=self.ids.formfield_passphrasehint.text.strip(),
        )

    def validate_form_values(self, form_values):
        form_error = None
        form_values_max_length = {
            key: len(value) for key, value in form_values.items() if len(value) > MAX_WA_CHARFIELD_LENGTH
        }
        if not all(form_values.values()):
            form_error = tr._("Please enter a username, passphrase and passphrase hint.")
        elif form_values_max_length:
            form_error = (
                tr._("Username, passphrase and passphrase hint must not exceed %s characters") % MAX_WA_CHARFIELD_LENGTH
            )
        elif len(form_values["keystore_passphrase"]) < PASSPHRASE_MIN_LENGTH and not form_values[
            "keystore_passphrase"
        ].startswith(
            "¤"
        ):  # HACK to have short passwords for tests
            form_error = tr._("Passphrase must be at least %s characters long.") % PASSPHRASE_MIN_LENGTH

        if form_error:
            raise ValueError(form_error)

    def request_authenticator_initialization(self):
        form_values = self.get_form_values()

        try:
            self.validate_form_values(form_values)
        except ValueError as exc:
            self.open_generic_dialog(str(exc), title=tr._("Validation error"))
            return

        self._launch_authenticator_initialization(form_values=form_values)

    def open_generic_dialog(self, text, title, on_dismiss=None):
        dialog_with_close_button(title=title, text=text, **({"on_dismiss": on_dismiss} if on_dismiss else {}))

    # No safe_catch_unhandled_exception_and_display_popup() here, we handle finalization in any case
    @process_method_with_gui_spinner
    def _offloaded_initialize_authenticator(self, form_values, authenticator_dir):

        logger.debug("Starting offloaded initialization of authenticator")

        success = False

        with catch_and_log_exception("AuthenticatorCreationFormScreen._offloaded_initialize_authenticator"):

            Clock.schedule_once(partial(self._do_update_progress_bar, 10))

            initialize_authenticator(
                authenticator_dir,
                keystore_owner=form_values["keystore_owner"],
                keystore_passphrase_hint=form_values["keystore_passphrase_hint"],
            )

            filesystem_keystore = FilesystemKeystore(authenticator_dir)

            for i in range(1, GENERATED_KEYS_COUNT + 1):
                # TODO add some logging here
                key_pair = generate_keypair(key_algo="RSA_OAEP", passphrase=form_values["keystore_passphrase"])
                filesystem_keystore.set_keypair(
                    keychain_uid=generate_uuid0(),
                    key_algo="RSA_OAEP",
                    public_key=key_pair["public_key"],
                    private_key=key_pair["private_key"],
                )

                Clock.schedule_once(partial(self._do_update_progress_bar, 10 + int(i * 90 / GENERATED_KEYS_COUNT)))

            success = True

        Clock.schedule_once(partial(self.finish_initialization, success=success))

        logger.debug("Finished offloaded initialization of authenticator")

    def set_form_fields_status(self, enabled):

        form_ids = self.ids
        form_fields = [form_ids.formfield_username, form_ids.formfield_passphrase, form_ids.formfield_passphrasehint]

        for text_field in form_fields:
            text_field.focus = False
            text_field.disabled = not enabled
            # Unfocus triggered an animation, we must disable it
            Animation.cancel_all(text_field, "fill_color", "_line_width", "_hint_y", "_hint_lbl_font_size")
            if enabled:
                text_field.text = ""  # RESET

    def update_progress_bar(self, percent):
        Clock.schedule_once(partial(self._do_update_progress_bar, percent))

    def _do_update_progress_bar(self, percent, *args, **kwargs):
        self.ids.progress_bar.value = percent

    @safe_catch_unhandled_exception_and_display_popup
    def _launch_authenticator_initialization(self, form_values):

        logger.debug("Requesting initialization of authenticator")

        authenticator_dir = self.selected_authenticator_dir
        assert authenticator_dir, authenticator_dir  # Should have been transmitted to this Screen

        if not authenticator_dir.is_dir():
            authenticator_dir.mkdir(parents=False)  # Only 1 level of folder can be created here!
        assert authenticator_dir and authenticator_dir.is_dir(), authenticator_dir

        self.ids.button_initialize.disabled = True
        self.ids.formfield_passphrase.text = "***"  # PRIVACY
        self.operation_status = tr._("Please wait, generation of cryptographic keys might take a few minutes.")

        self.set_form_fields_status(enabled=False)
        self.ids.initialization_form_toolbar.disabled = True

        MONOTHREAD_POOL_EXECUTOR.submit(
            self._offloaded_initialize_authenticator, form_values=form_values, authenticator_dir=authenticator_dir
        )

    def finish_initialization(self, *args, success, **kwargs):
        if success:
            self.open_generic_dialog(
                tr._("Initialization successfully completed."),
                title=tr._("Success"),
                on_dismiss=lambda x: self.go_to_home_screen(),
            )
        else:
            self.open_generic_dialog(
                tr._("Operation failed, check logs."),
                title=tr._("Failure"),
                on_dismiss=lambda x: self.go_to_home_screen(),
            )

    def display_help_popup(self):
        authenticator_creation_form_help_text = (
            tr._(
                """On this page, you can initialize an authenticator inside an empty folder; this authenticator actually consists in metadata files as well as a set of asymmetric keypairs."""
            )
            + LINEBREAK * 2
            + tr._(
                """To proceed, you have to input your user name or pseudo, a long passphrase (e.g. consisting of 4 different words), and a public hint to help your remember your passphrase later."""
            )
            + LINEBREAK * 2
            + tr._(
                """You should keep your passphrase somewhere safe (in a digital password manager, on a paper in a vault...), because if you forget any of its aspects (upper/lower case, accents, spaces...), there is no way to recover it."""
            )
        )

        help_text_popup(title=tr._("Authenticator creation page"), text=authenticator_creation_form_help_text)
