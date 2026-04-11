import arcade

from src.views import MenuView
from src.utils import Config, ConfigKey


def main():
    """Main function"""
    config = Config()
    window = arcade.Window(
        Config.get(ConfigKey.WINDOW_WIDTH, 800),
        Config.get(ConfigKey.WINDOW_HEIGHT, 600),
        Config.get(ConfigKey.TITLE, "My Game")
    )

    menu = MenuView()

    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()