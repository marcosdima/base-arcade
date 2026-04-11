import arcade
import arcade.gui
from ..base import BaseView
from .game import GameView


class MenuView(BaseView):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()

    def on_show_view(self):
        self.ui.enable()
        self.ui.clear()

        arcade.set_background_color(arcade.color.BLACK)

        vbox = arcade.gui.UIBoxLayout(space_between=10)

        start_button = arcade.gui.UIFlatButton(text="Start", width=200)
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        start_button.on_click = self.on_click_start
        quit_button.on_click = self.on_click_quit

        vbox.add(start_button)
        vbox.add(quit_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=vbox,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        self.ui.add(anchor)


    def on_hide_view(self):
        self.ui.disable()


    def on_click_start(self, event):
        self.window.show_view(GameView())


    def on_click_quit(self, event):
        arcade.close_window()


    def on_draw(self):
        self.clear()
        self.ui.draw()