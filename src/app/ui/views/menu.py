import arcade

from ....engine.ui import BaseView, UIElementProps
from ....engine.ui.components import Button, ButtonProps


class MenuView(BaseView):
    def on_show_view(self):
        super().on_show_view()

        print('Showing menu view')

        # Set button properties.
        quit_button_props = ButtonProps(
            text='Quit',
            on_click=self.on_click_quit,
        )

        # Create quit button.
        print(self.window.width, self.window.height)
        quit_button = Button(
            props=UIElementProps(
                rect=(self.window.width / 2, self.window.height / 2, 100, 50),
                name='quit_button',
            ),
            button_props=quit_button_props,
        )
        self.root.add_child(quit_button)

    def on_click_quit(self, event):
        arcade.close_window()
