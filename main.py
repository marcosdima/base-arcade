import arcade

from src.app import App
from src.services import Config, ConfigKey, Lang

config = Config()
lang = Lang(default_language=Config.get(ConfigKey.LANGUAGE, 'en'))

window = arcade.Window(
    Config.get(ConfigKey.WINDOW_WIDTH, 800),
    Config.get(ConfigKey.WINDOW_HEIGHT, 600),
    Config.get(ConfigKey.TITLE, 'My Game'),
)


def main():
    # Subscribe to config changes to update the window when necessary.
    config.field_changed.subscribe(on_config_change)

    # Initialize the application.
    app = App(window)
    arcade.run()


def on_config_change(key: ConfigKey, value):
    if key in [ConfigKey.WINDOW_WIDTH, ConfigKey.WINDOW_HEIGHT]:
        window.set_size(
            value
            if key == ConfigKey.WINDOW_WIDTH
            else Config.get(ConfigKey.WINDOW_WIDTH, 800),
            value
            if key == ConfigKey.WINDOW_HEIGHT
            else Config.get(ConfigKey.WINDOW_HEIGHT, 600),
        )
        print(window.size, value)
    elif key == ConfigKey.TITLE:
        window.set_caption(Config.get(ConfigKey.TITLE, 'My Game'))


if __name__ == '__main__':
    main()
