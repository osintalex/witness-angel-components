import pprint
import uuid
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from textwrap import dedent

from functools import partial
from uuid import UUID

from Crypto.Random import get_random_bytes
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from wacryptolib.exceptions import ExistenceError, KeyDoesNotExist
from wacryptolib.jsonrpc_client import JsonRpcProxy, status_slugs_response_error_handler

from wacomponents.screens.authenticator_management import shorten_uid
from wacomponents.widgets.popups import dialog_with_close_button, process_method_with_gui_spinner, register_current_dialog, \
    close_current_dialog, help_text_popup
from wacryptolib.authenticator import initialize_authenticator, load_authenticator_metadata
from wacryptolib.key_generation import generate_asymmetric_keypair
from wacryptolib.key_storage import FilesystemKeyStorage
from wacryptolib.utilities import generate_uuid0, load_from_json_file, get_metadata_file_path

from wacomponents.i18n import tr

import requests

Builder.load_file(str(Path(__file__).parent / 'authenticator_synchronization_form.kv'))

THREAD_POOL_EXECUTOR = ThreadPoolExecutor(
    max_workers=1, thread_name_prefix="authenticator_keygen_worker"  # SINGLE worker for now, to avoid concurrency
)

GENERATED_KEYS_COUNT = 7
PASSPHRASE_MIN_LENGTH = 20


class AuthenticatorDoesNotExist(ExistenceError):  # TODO add this in exceptions.py of cryptolib project
    pass


class AuthenticatorAlreadyExists(ExistenceError):  # TODO add this in exceptions.py of cryptolib project
    pass


class AuthenticatorSynchronizationScreen(Screen):
    selected_authenticator_dir = ObjectProperty(None, allownone=True)

    synchronization_status = StringProperty()
    is_synchronized = ObjectProperty(None, allownone=True)

    jsonrpc_url = "http://127.0.0.1:8000" + "/json/"  # FIXME change url!!

    escrow_proxy = JsonRpcProxy(
        url=jsonrpc_url, response_error_handler=status_slugs_response_error_handler
    )

    report = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = MDApp.get_running_app()

    def go_to_home_screen(self):
        self.manager.current = "authenticator_selector_screen"

    def open_dialog(self, text, title, on_dismiss=None):
        dialog_with_close_button(
            title=title,
            text=text,
            **({"on_dismiss": on_dismiss} if on_dismiss else {})
        )

    def close_dialog(self, obj):
        close_current_dialog()

    def close_dialog_and_leave(self, obj):
        close_current_dialog()
        self.go_to_home_screen()

    def _query_remote_athenticator_status(self, username: str, authenticator_secret: str):
        gateway = "http://127.0.0.1:8000"

        # try:
        # response = requests.get(gateway)
        # response.raise_for_status()

        # access Json content
        # remote_metadata_status = response.json()

        # except requests.exceptions.HTTPError as e:  # TODO manage only the case where the http error is 404
        # is_synchronized = None
        # raise AuthenticatorDoesNotExist("Authenticator does not exist".format(e))from e

        try:
            public_authenticator = self.escrow_proxy.get_public_authenticator_view(username=username,
                                                                                   authenticator_secret=authenticator_secret)
            self.is_synchronized = None
            remote_metadata_status = {
                'device_uid': public_authenticator['username'],
                'public_keys': public_authenticator['public_keys'],
                'user': public_authenticator['description']
            }

        except ExistenceError:
            self.is_synchronized = True
            remote_metadata_status = {
                'device_uid': '',
                'public_keys': '',
                'user': ''
            }

        return remote_metadata_status, self.is_synchronized

    @staticmethod
    def _compare_local_and_remote_status(local_metadata_status, remote_metadata_status, is_synchronized) -> dict:

        local_keys_tuple = [(public_key["keychain_uid"], public_key["key_type"]) for public_key in
                            local_metadata_status["public_keys"]]

        remote_keys_tuple = [(public_key["keychain_uid"], public_key["key_type"]) for public_key in
                             remote_metadata_status["public_keys"]]

        missing_public_keys_in_remote = set(local_keys_tuple) - set(remote_keys_tuple)
        exceeding_public_keys_in_remote = set(remote_keys_tuple) - set(local_keys_tuple)

        if not missing_public_keys_in_remote and not exceeding_public_keys_in_remote:
            is_synchronized = False

        report = dict(
            missing_keys_in_remote=missing_public_keys_in_remote,
            exceeding_keys_in_remote=exceeding_public_keys_in_remote,
            is_synchronized=is_synchronized)

        return report

    def refresh_status(self):

        authenticator_path = self.selected_authenticator_dir

        authenticator_metadata = load_authenticator_metadata(authenticator_path)
        filesystem_key_storage = FilesystemKeyStorage(authenticator_path)
        local_keys_status = filesystem_key_storage.list_keypair_identifiers()
        for x in local_keys_status:
            del x["private_key_present"]

        local_keys_and_authenticator_metadata_reformatted = {
            'device_uid': authenticator_metadata["device_uid"],
            'user': authenticator_metadata["user"],
            'public_keys': local_keys_status
        }

        device_uid = str(authenticator_metadata["device_uid"])
        secret_key_uuid = str(authenticator_metadata["secret_key_uuid"])

        remote_metadata_status, self.is_synchronized = self._query_remote_athenticator_status(username=device_uid,
                                                                                              authenticator_secret=secret_key_uuid)

        self.report = self._compare_local_and_remote_status(local_keys_and_authenticator_metadata_reformatted,
                                                            remote_metadata_status, self.is_synchronized)

        # pprint.pprint(report)

        is_synchronized = self.report["is_synchronized"]

        if is_synchronized is None:
            synchronization_status = tr._("PUBLISHED")
            message = tr._("Incohérence detectée entre les versions locale et distante")

        elif not is_synchronized:
            synchronization_status = tr._("PUBLISHED")
            message = tr._("Authentfieur local est bien à jour")
        else:
            synchronization_status = tr._("NOT PUBLISHED")
            message = tr._("Authentfieur local n'existe pas sur le depôt distant")

        exceeding_public_keys_cast = [shorten_uid(k[0]) for k in self.report["exceeding_keys_in_remote"]]
        missing_public_keys_cast = [shorten_uid(k[0]) for k in self.report["missing_keys_in_remote"]]

        displayed_values = dict(
            gateway="https://witnessangel.com/",
            status=synchronization_status,
            message=message,
            exceeding_keys_in_remote=(", ".join(exceeding_public_keys_cast) or "-"),
            missing_keys_in_remote=(", ".join(missing_public_keys_cast) or "-"),
        )

        synchronization_info_text = dedent(tr._("""\
                        Gateway : {gateway}
                        Remote status : {status}
                        Message : {message}
                        Details : 
                                Exceeding keys in remote : {exceeding_keys_in_remote}
                                Missing keys in remote : {missing_keys_in_remote}
                    """)).format(**displayed_values)

        textarea = self.ids.synchronization_information
        textarea.text = synchronization_info_text

        self.is_synchronized = is_synchronized

        # print("self is synchronized :", repr(self.is_synchronized), type(self.is_synchronized))

    def synchronize_keys(self):
        public_keys = []
        if self.report["missing_keys_in_remote"]:
            authenticator_path = self.selected_authenticator_dir
            authenticator_metadata = load_authenticator_metadata(authenticator_path)
            print(self.report)
            for missing_key in self.report["missing_keys_in_remote"]:
                public_keys.append({
                    "keychain_uid": missing_key[0],
                    "key_type": missing_key[1],
                    "payload": b"azertyuiopppp"
                })

            self.escrow_proxy.set_public_authenticator_view(username=authenticator_metadata["device_uid"],
                                                            description=authenticator_metadata["user"],
                                                            authenticator_secret=authenticator_metadata[
                                                                "secret_key_uuid"],
                                                            public_keys=public_keys)

            self.refresh_status()

    def update_progress_bar(self, percent):
        Clock.schedule_once(partial(self._do_update_progress_bar, percent))

    def _do_update_progress_bar(self, percent, *args, **kwargs):
        self.ids.progress_bar.value = percent

    def _launch_synchronization_initialization(self, form_values):
        authenticator_path = self.selected_authenticator_dir
        assert authenticator_path and authenticator_path.is_dir(), authenticator_path

        self.ids.button_initialize.disabled = True
        self.ids.formfield_passphrase.text = "***"  # PRIVACY
        self.operation_status = tr._("Please wait, initialization might take a few minutes.")

        self.set_form_fields_status(enabled=False)
        self.ids.initialization_form_toolbar.disabled = True

        THREAD_POOL_EXECUTOR.submit(self._offloaded_initialize_authenticator,
                                    form_values=form_values,
                                    authenticator_path=authenticator_path)

    def display_help_popup(self):
        help_text = dedent(tr._("""\
        On this page, you can initialize an authenticator inside an empty folder; this authenticator actually consists in metadata files as well as a set of asymmetric keypairs.

        To proceed, you have to input your user name or pseudo, a long passphrase (e.g. consisting of 4 different words), and a public hint to help your remember your passphrase later.

        You should keep your passphrase somewhere safe (in a digital password manager, on a paper in a vault...), because if you forget any of its aspects (upper/lower case, accents, spaces...), there is no way to recover it.
        """))
        help_text_popup(
            title=tr._("Authenticator creation page"),
            text=help_text, )
