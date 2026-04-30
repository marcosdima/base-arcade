from .router import Router
from .ui.views import MenuView


class App:
    def __init__(self, window):
        self.window = window

        # View management.
        self.main_menu_view = MenuView()

        self.router = Router(
            window=self.window,
            routes={
                'main_menu': lambda: self.main_menu_view,
            },
            initial='main_menu',
        )
