import arcade
import arcade.gui
from ..base import BaseView
from ...handlers import Lang


class PauseView(BaseView):
    def __init__(self, comes_from: BaseView):
        super().__init__()
        self.comes_from = comes_from
        self.ui = arcade.gui.UIManager()
        self.keyboard_handler.on_escape_pressed.subscribe(self.return_to)
        

    def on_show_view(self):
        self.ui.enable()
        self.ui.clear()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        vbox = arcade.gui.UIBoxLayout(space_between=10)
        title_label = arcade.gui.UILabel(text=Lang.get('pause.title'), font_size=36)

        w = self.window.width
        menu_button = arcade.gui.UIFlatButton(text=Lang.get('pause.main_menu'), width=int(w * 0.3))
        settings_button = arcade.gui.UIFlatButton(text=Lang.get('pause.settings'), width=int(w * 0.3))
        resume_button = arcade.gui.UIFlatButton(text=Lang.get('pause.resume'), width=int(w * 0.3))

        menu_button.on_click = self.on_click_main_menu
        settings_button.on_click = self.on_click_settings
        resume_button.on_click = self.on_click_resume

        vbox.add(title_label)
        vbox.add(menu_button)
        vbox.add(settings_button)
        vbox.add(resume_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=vbox,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        self.ui.add(anchor)


    def on_hide_view(self):
        self.ui.disable()


    def on_draw(self):
        self.clear()
        self.ui.draw()


    def on_click_main_menu(self, event):
        from .menu import MenuView
        self.window.show_view(MenuView())


    def on_click_settings(self, event):
        # TODO: Replace with a dedicated settings view when implemented.
        pass


    def on_click_resume(self, event):
        self.return_to()


    def return_to(self):
        self.window.show_view(self.comes_from)