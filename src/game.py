import arcade

from .areas import Area
from .utils import Config, ConfigKey
from .entities import Entity, Player
from .handlers import InputHandler


class GameView(arcade.View):
    """
    Main application class.
    """
    def __init__(self, window: arcade.Window):
        super().__init__(
            window,
            Config.get(ConfigKey.BACKGROUND_COLOR, arcade.color.WHITE),
        )

        # Instantiate attributes.
        self.camera_sprites = arcade.Camera2D()
        self.camera_gui = arcade.Camera2D()
        self.main_scene = arcade.Scene()
        self.inputs = InputHandler()    
        self.player = Player(input=self.inputs)
        self.areax = Area(100, 100, 200, 200)
        

        # Add the player to the main scene.
        self.main_scene.add_sprite(self.player.name, self.player)
        self.main_scene.add_sprite("areax", self.areax.sprite)


    def on_show_view(self):
        # Called when this view becomes active.
        pass


    def on_draw(self):
        # Called every frame to render the screen.
        self.clear()
        self.main_scene.draw()
        self.main_scene.draw_hit_boxes(color=arcade.color.RED, line_thickness=1)

        for sprite_list in self.main_scene._sprite_lists:
            for sprite in sprite_list:
                if isinstance(sprite, Entity):
                    sprite.draw_name()
        

    def on_update(self, delta_time: float):
        # Called every frame to update game logic.
        self.player.update(delta_time)
        self.areax.update([self.player])


    def on_key_press(self, key: int, modifiers: int):
        # Called when a keyboard key is pressed.
        self.inputs.key_pressed(key)


    def on_key_release(self, key: int, modifiers: int):
        # Called when a keyboard key is released.
        self.inputs.key_released(key)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Called when a mouse button is pressed.
        pass


    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        # Called when a mouse button is released.
        pass

    
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # Called when the mouse moves.
        self.inputs.update_mouse(x, y, dx, dy)