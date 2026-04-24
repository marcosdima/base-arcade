import arcade
import arcade.gui
from ...services import Lang
from .app_view import AppView


class MenuView(AppView):
    def on_show_view(self):
        super().on_show_view()
        
        arcade.set_background_color(arcade.color.BLACK)

        vbox = arcade.gui.UIBoxLayout(space_between=10)
        title_label = arcade.gui.UILabel(text=Lang.get('main_menu.title'), font_size=36)

        w = self.window.width
        start_button = arcade.gui.UIFlatButton(text=Lang.get('main_menu.start'), width=int(w * 0.3))
        leaderboard_button = arcade.gui.UIFlatButton(text=Lang.get('main_menu.leaderboard'), width=int(w * 0.3))
        quit_button = arcade.gui.UIFlatButton(text=Lang.get('main_menu.quit'), width=int(w * 0.3))

        start_button.on_click = lambda event: self.router.navigate("game")
        leaderboard_button.on_click = lambda event: self.router.navigate("leaderboard")
        quit_button.on_click = self.on_click_quit

        vbox.add(title_label)
        vbox.add(start_button)
        vbox.add(leaderboard_button)
        vbox.add(quit_button)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=vbox,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        self.ui.add(anchor)


    def on_click_quit(self, event):
        arcade.close_window()


    