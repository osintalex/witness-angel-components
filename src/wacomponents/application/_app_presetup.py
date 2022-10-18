

def _presetup_app_environment(setup_kivy):
    """Setup for both gui and console apps."""
    import os

    os.environ["KIVY_NO_ARGS"] = "1"  # Important to bypass Kivy CLI system

    try:

        protected_app_package = os.getenv("ENABLE_TYPEGUARD")
        if protected_app_package:
            from typeguard.importhook import install_import_hook
            install_import_hook(protected_app_package)

    except Exception as exc:
        print(">>>>>>>> FAILED INITIALIZATION OF TYPEGUARD: %r" % exc)

    try:

        from wacomponents.default_settings import IS_ANDROID, IS_MOBILE
        from wacomponents.application.android_helpers import patch_ctypes_module_for_android
        if IS_ANDROID:
            patch_ctypes_module_for_android()  # Necessary for wacryptolib

            from jnius import autoclass
            from android.runnable import Runnable

            def config_real():
                python_activity_class = autoclass("org.kivy.android.PythonActivity")
                python_activity_instance = python_activity_class.mActivity
                android_window = python_activity_instance.getWindow()
                android_window.addFlags(2)  # Constant LAYOUT_IN_DISPLAY_CUTOUT_MODE_NEVER
                print(">>>>>>>> Called android_window.addFlags(LAYOUT_IN_DISPLAY_CUTOUT_MODE_NEVER) !")
            Runnable(config_real)()

    except Exception as exc:
        print(">>>>>>>> FAILED ANDROID PRESETUP: %r" % exc)

    try:

        # Add paths to image/font/sound assets, for e-paper too!
        from wacomponents.assets import register_common_resources
        register_common_resources()

    except Exception as exc:
        print(">>>>>>>> FAILED REGISTERING COMMON RESOURCES: %r" % exc)

    if not setup_kivy:
        return  # Cancel the rest of setups

    try:

        # WORKAROUND FOR LOGGING AND GRAPHICS WEIRDNESS IN KIVY SETUP #

        import logging
        import sys
        custom_kivy_stream_handler = logging.StreamHandler()
        sys._kivy_logging_handler = custom_kivy_stream_handler
        from kivy.logger import Logger as logger  # Trigger init of Kivy logging
        del logger

        # Finish ugly monkey-patching by Kivy
        assert logging.getLogger("kivy") is logging.root
        logging.Logger.root = logging.root
        logging.Logger.manager.root = logging.root

        # For now allow EVERYTHING
        logging.root.setLevel(logging.INFO)
        logging.disable(0)

        # import logging_tree
        # logging_tree.printout()

    except Exception as exc:
        print(">>>>>>>> FAILED INITIALIZATION OF KIVY LOGGING: %r" % exc)

    try:

        # SETUP THE APP WINDOW AND ITS HELPERS

        from wacomponents.default_settings import IS_MOBILE

        from kivy.config import Config
        '''
        Config.set('graphics', 'top', '50')
        Config.set('graphics', 'left', '50')
        Config.set('graphics', 'position', 'custom')
        '''
        # FIXME this happens too late it seems
        #Config.set("graphics", "fullscreen", "0")
        #Config.set("graphics", "show_cursor", "1")

        from kivy.core.window import Window
        ##Window.minimum_width, Window.minimum_height = Window.size = (600, 600)

        if not IS_MOBILE:
            # Disable multitouch emulation red dots on Desktop, on right/middle clicks
            Config.set('input', 'mouse', 'mouse,disable_multitouch,disable_on_activity')

        # HACK TO TEMPORARILY EMULATE TOUCHSCREEN ON DESKTOP:
        #Config.set('kivy', 'desktop', 0)

        # HACK to ensure that we don't need to click TWICE to gain focus on Kivy Window and then on widget!
        # https://stackoverflow.com/questions/53337630/kivy-on-windows10-how-to-click-a-button-when-kivy-application-does-not-in-focu
        def force_window_focus(*args, **kwargs):
            Window.raise_window()
        Window.bind(on_cursor_enter=force_window_focus)

        from wacomponents.widgets.layout_components import load_layout_helper_widgets
        load_layout_helper_widgets()

    except Exception as exc:
        print(">>>>>>>> FAILED INITIALIZATION OF KIVY WINDOW AND ASSETS: %r" % exc)
        raise

