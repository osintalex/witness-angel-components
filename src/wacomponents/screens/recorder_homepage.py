from pathlib import Path

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen

from wacomponents.widgets.layout_components import LanguageSwitcherScreenMixin

Builder.load_file(str(Path(__file__).parent / 'recorder_homepage.kv'))



class RecorderHomepageScreen(LanguageSwitcherScreenMixin, Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app = MDApp.get_running_app()

    def on_language_change(self, lang_code):
        super().on_language_change(lang_code)
        self._app.refresh_checkup_status()  # Refresh translation of Drive etc.
