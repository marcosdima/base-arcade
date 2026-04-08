import arcade

from src.game import GameView
from src.utils import Config, ConfigKey

CONFIG = Config()

def main():
    """Main function"""
    config = Config()
    window = arcade.Window(
        Config.get(ConfigKey.WINDOW_WIDTH, 800),
        Config.get(ConfigKey.WINDOW_HEIGHT, 600),
        Config.get(ConfigKey.TITLE, "My Game")
    )
    game = GameView(window=window)

    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()