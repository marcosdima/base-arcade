from ..engine.core import Font
from ..engine.ui import Style, UIElement, UIElementProps
from .router import Router
from .ui.views import MenuView


class App:
    def __init__(self, window):
        self.window = window

        self.app_root = UIElement(
            props=UIElementProps(
                rect=(0, 0, self.window.width, self.window.height),
                style=Style(
                    font=Font(name='Arial', size=14, font_color='red'),
                ),
                name='app_root',
                debug=False,
            ),
        )

        # View management.
        self.main_menu_view = MenuView(root=self.app_root)

        self.router = Router(
            window=self.window,
            routes={
                'main_menu': lambda: self.main_menu_view,
            },
            initial='main_menu',
        )
