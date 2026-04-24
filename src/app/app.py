from .views import *
from .router import Router

class App:
    def __init__(self, window):
        self.window = window

        # View management.
        self.main_menu_view = MenuView()
        self.game_view = GameView()
        self.pause_view = lambda: PauseView(comes_from=self.window.current_view)

        self.router = Router(
            window=self.window,
            routes={
                "main_menu": lambda: self.main_menu_view,
                "pause": PauseView,
                "leaderboard": LeaderboardView,
                "game": lambda: self.game_view,
            },
            initial="main_menu"
        )


        