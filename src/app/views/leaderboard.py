import arcade
import arcade.gui
from ...services import Lang, Leaderboard
from .app_view import AppView


class LeaderboardView(AppView):
    def setup(self):
        super().setup()
        self.keyboard_handler.on_escape_pressed.subscribe(lambda: self.router.go_back())
        self.leaderboard = Leaderboard()
        

    def on_show_view(self):
        super().on_show_view()
        
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

        menu_button.on_click = lambda event: self.router.navigate("main_menu")
        settings_button.on_click = lambda event: self.router.navigate("settings")
        resume_button.on_click = lambda event: self.router.go_back()

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


    def on_click_settings(self, event):
        # TODO: Replace with a dedicated settings view when implemented.
        pass
