from arcade import color, Scene, SpriteList, PhysicsEngineSimple
from ..base import BaseView
from ...game import Entity, Player, Area


class GameView(BaseView):
    def __init__(self):
        super().__init__()

        # Set main scene.
        self.main_scene = Scene()

        # Test player and areas.
        self.player = Player(mouse=self.mouse_handler, keyboard=self.keyboard_handler)
        self.areax = Area(x=300, y=300, width=200, height=200)
        
        # Add the player to the main scene.
        self.main_scene.add_sprite(self.player.body.name, self.player.body)
        self.main_scene.add_sprite("areax", self.areax.sprite)

        # Collision tests.
        self.obstacles = SpriteList(use_spatial_hash=True)
        obstacle1 = Entity('Obstacle1', (100, 100))
        obstacle1.center_x = 200
        obstacle1.center_y = 300
        self.obstacles.append(obstacle1)
        self.main_scene.add_sprite(obstacle1.name, obstacle1)

        # Physics engine for player movement and collision with obstacles.
        self.physics_engine = PhysicsEngineSimple(
            self.player.body,
            self.obstacles
        )


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
        self.areax.update([self.player.body])
        self.main_scene.update(delta_time)
        self.physics_engine.update()