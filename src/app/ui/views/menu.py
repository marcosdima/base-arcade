import arcade

from ....engine.core import Font
from ....engine.ui import BaseView, Border, Style, UIElementProps, UIStateValue
from ....engine.ui.components import Button, ButtonProps
from ...themes import MANAGER as ThemeManager


class MenuView(BaseView):
    def on_show_view(self):
        super().on_show_view()

        print('Showing menu view')
        ThemeManager.change_theme('light')

        # Create quit button.
        self.quit_button = Button(
            props=UIElementProps(
                rect=(self.window.width / 2, self.window.height / 2, 100, 50),
                name='quit_button',
                debug=False,
                style={
                    UIStateValue.ACTIVE: Style(
                        background_color='red',
                        font=Font(name='Roboto', size=20),
                        border=Border(width=3, color='black', radius=5),
                    ),
                    UIStateValue.HOVER: Style(
                        background_color='dark_red',
                        font=Font(name='Roboto', size=20, color='yellow'),
                        border=Border(width=3, color='yellow', radius=5),
                    ),
                    UIStateValue.CLICKED: Style(
                        background_color='green',
                        font=Font(name='Roboto', size=20, color='white'),
                        border=Border(width=3, color='black', radius=5),
                    ),
                },
            ),
            button_props=ButtonProps(
                text='Quit',
                on_click=self.on_click_quit,
            ),
        )

        self.root.add_child(self.quit_button)

    def on_click_quit(self):
        arcade.close_window()
