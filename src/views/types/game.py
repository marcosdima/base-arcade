from ..base import BaseView
from ...game import Entity, Player, Area, World, WorldTag
from ...utils import Interaction


class GameView(BaseView):
    def __init__(self):
        super().__init__()

        # Set world and area scene.
        self.world = World()

        # Test player and areas.
        self.player = Player(mouse=self.mouse_handler, keyboard=self.keyboard_handler)
        self.player.body.center_x = 100
        self.player.body.helpers.tags.add(WorldTag.DYNAMIC.value)
        self.world.add_entity(self.player.body)
        self.area1 = self._setup_area_1()
        self.area2 = self._setup_area_2()

        # Collision tests.
        obstacle1 = Entity('Obstacle1', (50, 50))
        obstacle1.center_x = 300
        obstacle1.center_y = 500
        obstacle1.helpers.tags.add(WorldTag.STATIC.value)
        self.world.add_entity(obstacle1)

        enemy = Entity('Enemy', (36, 36))
        enemy.helpers.tags.add(WorldTag.DYNAMIC.value)
        self.world.add_entity(enemy)
        enemy.helpers.movement.speed = 100
        enemy.helpers.movement.physics = self.world.physics
        enemy.helpers.activate_follow()
        enemy.helpers.follow.follow(self.player.body, distance=150)

        # Subscribe to pause menu event.
        self.keyboard_handler.on_escape_pressed.subscribe(self.go_to_pause_menu)


    def on_draw(self):
        # Called every frame to render the screen.
        self.clear()
        self.world.draw()


    def on_update(self, delta_time: float):
        # Called every frame to update game logic.
        self.world.update(delta_time)
        self.area1.update([self.player.body])
        self.area2.update([self.player.body])


    def go_to_pause_menu(self):
        from .pause import PauseView
        self.window.show_view(PauseView(self))


    def _setup_area_1(self):
        area = Area(x=300, y=300, width=200, height=200)
        interaction = Interaction(
            name="Test Interaction",
            action=lambda: print("Interaction 1 executed!"),
            priority=1,
            on_focus=lambda: print("Interaction 1 focused!"),
            on_blur=lambda: print("Interaction 1 blurred!")
        )

        def _on_player_enter_area(player_body: Entity):
            if player_body != self.player.body:
                return
            player_body.helpers.interact.add(interaction)

        def _on_player_exit_area(player_body: Entity):
            if player_body != self.player.body:
                return
            player_body.helpers.interact.remove(interaction)

        area.on_enter.subscribe(_on_player_enter_area)
        area.on_exit.subscribe(_on_player_exit_area)
        self.world.add_area(area)

        return area


    def _setup_area_2(self):
        area = Area(x=400, y=300, width=200, height=200)
        interaction = Interaction(
            name="Test Interaction",
            action=lambda: print("Interaction 2 executed!"),
            priority=1,
            on_focus=lambda: print("Interaction 2 focused!"),
            on_blur=lambda: print("Interaction 2 blurred!")
        )

        def _on_player_enter_area(player_body: Entity):
            if player_body != self.player.body:
                return
            player_body.helpers.interact.add(interaction)

        def _on_player_exit_area(player_body: Entity):
            if player_body != self.player.body:
                return
            player_body.helpers.interact.remove(interaction)

        area.on_enter.subscribe(_on_player_enter_area)
        area.on_exit.subscribe(_on_player_exit_area)
        self.world.add_area(area)

        return area
