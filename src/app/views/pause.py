import arcade
import arcade.gui

from ...services import Lang
from .app_view import AppView


class PauseView(AppView):
    def setup(self):
        super().setup()
        self.keyboard_handler.on_escape_pressed.subscribe(self.return_to)

    def on_show_view(self):
        super().on_show_view()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        vbox = arcade.gui.UIBoxLayout(space_between=10)
        title_label = arcade.gui.UILabel(text=Lang.get('pause.title'), font_size=36)

        w = self.window.width
        menu_button = arcade.gui.UIFlatButton(
            text=Lang.get('pause.main_menu'), width=int(w * 0.3)
        )
        settings_button = arcade.gui.UIFlatButton(
            text=Lang.get('pause.settings'), width=int(w * 0.3)
        )
        resume_button = arcade.gui.UIFlatButton(
            text=Lang.get('pause.resume'), width=int(w * 0.3)
        )

        menu_button.on_click = lambda event: self.router.navigate('main_menu')
        settings_button.on_click = lambda event: self.router.navigate('settings')
        resume_button.on_click = lambda event: self.router.go_back()

        vbox.add(title_label)
        vbox.add(menu_button)
        vbox.add(settings_button)
        vbox.add(resume_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=vbox,
            anchor_x='center_x',
            anchor_y='center_y',
        )

        self.ui.add(anchor)

    def return_to(self):
        self.router.go_back()
