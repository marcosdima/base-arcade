from .views import *


class App:
    def __init__(self, window):
        self.window = window

        # View management.
        self.main_menu_view = MenuView()
        self.pause_view = lambda: PauseView(comes_from=self.window.current_view)