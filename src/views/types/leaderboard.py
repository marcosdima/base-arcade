import arcade
import arcade.gui
from ..base import BaseView
from ...handlers import Lang, Leaderboard
from ...utils import resource_path


class LeaderboardView(BaseView):
    def __init__(self, comes_from: BaseView):
        super().__init__()
        self.comes_from = comes_from
        self.ui = arcade.gui.UIManager()
        self.keyboard_handler.on_escape_pressed.subscribe(self.return_to)
        self.leaderboard = Leaderboard()
        

    def on_show_view(self):
        self.ui.enable()
        self.ui.clear()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Main vertical layout
        main_vbox = arcade.gui.UIBoxLayout(space_between=15)
        
        # Title
        title_label = arcade.gui.UILabel(text=Lang.get('leaderboard.title'), font_size=36)
        main_vbox.add(title_label)

        # Scores display
        scores_box = self._create_scores_box()
        main_vbox.add(scores_box)

        # Buttons
        w = self.window.width
        buttons_hbox = arcade.gui.UIBoxLayout(space_between=10, vertical=False)
        
        menu_button = arcade.gui.UIFlatButton(text=Lang.get('leaderboard.main_menu'), width=int(w * 0.25))
        settings_button = arcade.gui.UIFlatButton(text=Lang.get('leaderboard.settings'), width=int(w * 0.25))
        resume_button = arcade.gui.UIFlatButton(text=Lang.get('leaderboard.resume'), width=int(w * 0.25))

        menu_button.on_click = self.on_click_main_menu
        settings_button.on_click = self.on_click_settings
        resume_button.on_click = self.on_click_resume

        buttons_hbox.add(menu_button)
        buttons_hbox.add(settings_button)
        buttons_hbox.add(resume_button)
        
        main_vbox.add(buttons_hbox)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=main_vbox,
            anchor_x="center_x",
            anchor_y="center_y",
        )

        self.ui.add(anchor)


    def _create_scores_box(self) -> arcade.gui.UIWidget:
        """Crea la caja que muestra la tabla de scores."""
        scores_vbox = arcade.gui.UIBoxLayout(space_between=8)
        
        # Scores
        top_scores = self.leaderboard.get_top_scores(10)
        
        # Headers
        header_text = f"{'Rank':<6} {'Name':<20} {'Score':>10}"
        header_label = arcade.gui.UILabel(text=header_text, font_size=12, font_name="Arial")
        scores_vbox.add(header_label)
        
        # Separator
        separator = arcade.gui.UILabel(text="-" * 40, font_size=10, font_name="Arial")
        scores_vbox.add(separator)
        
        if not top_scores:
            scores_vbox.add(arcade.gui.UILabel(text="No scores yet", font_size=12))
        else:
            for idx, score_entry in enumerate(top_scores, 1):
                score_text = f"{idx:<6} {score_entry.get('name', 'Unknown'):<20} {score_entry.get('score', 0):>10}"
                score_label = arcade.gui.UILabel(text=score_text, font_size=12, font_name="Arial")
                scores_vbox.add(score_label)
        
        return scores_vbox


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