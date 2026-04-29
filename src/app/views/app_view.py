import arcade
import arcade.gui

from ...engine import BaseView
from ..router import Router


class AppView(BaseView):
    def __init__(self):
        super().__init__()
        self.router: Router = None
        self.ui = arcade.gui.UIManager()
        self.setup()

    def setup(self):
        pass

    def on_hide_view(self):
        super().on_hide_view()
        self.ui.disable()

    def on_show_view(self):
        super().on_show_view()
        self.ui.enable()
        self.ui.clear()

    def on_draw(self):
        super().on_draw()
        self.clear()
        self.ui.draw()
