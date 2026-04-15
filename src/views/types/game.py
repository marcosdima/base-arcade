from arcade import color, Scene, SpriteList, PhysicsEngineSimple
from ..base import BaseView
from ...game import Entity, Player, Area
from ...utils import Interaction


class GameView(BaseView):
    def __init__(self):
        super().__init__()

        # Set main scene.
        self.main_scene = Scene()

        # Test player and areas.
        self.player = Player(mouse=self.mouse_handler, keyboard=self.keyboard_handler)
        self.area1 = self._setup_area_1()
        self.area2 = self._setup_area_2()
        
        # Add the player to the main scene.
        self.main_scene.add_sprite(self.player.body.name, self.player.body)

        # Collision tests.
        self.obstacles = SpriteList(use_spatial_hash=True)
        obstacle1 = Entity('Obstacle1', (100, 100))
        obstacle1.center_x = 100
        obstacle1.center_y = 100
        self.obstacles.append(obstacle1)
        self.main_scene.add_sprite(obstacle1.name, obstacle1)

        # Physics engine for player movement and collision with obstacles.
        self.physics_engine = PhysicsEngineSimple(
            self.player.body,
            self.obstacles
        )

        # Subscribe to pause menu event.
        self.keyboard_handler.on_escape_pressed.subscribe(self.go_to_pause_menu)


    def on_draw(self):
        # Called every frame to render the screen.
        self.clear()
        self.main_scene.draw()
        self.main_scene.draw_hit_boxes(color=color.RED, line_thickness=1)

        for sprite_list in self.main_scene._sprite_lists:
            for sprite in sprite_list:
                if isinstance(sprite, Entity):
                    sprite.draw_name()


    def on_update(self, delta_time: float):
        # Called every frame to update game logic.
        self.area1.update([self.player.body])
        self.area2.update([self.player.body])
        self.main_scene.update(delta_time)
        self.physics_engine.update()


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
        self.main_scene.add_sprite("area1", area.sprite)

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
        self.main_scene.add_sprite("area2", area.sprite)

        return area
