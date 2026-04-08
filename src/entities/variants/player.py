import arcade
import math
from ...handlers import InputHandler
from ...utils import Config, ConfigKey
from ..entity import Entity


class Player(Entity): 
    def __init__(self, input: InputHandler):
        super().__init__(name="Player", color=arcade.color.GOLD, size=(100, 100))
        self.input = input
        self.movement_speed = 10
        self.look_offset = -90


    def update(self, delta_time: float, *args, **kwargs):
        # Handle player movement based on input.
        move_x = 0
        move_y = 0
        if self.input.is_pressed(Config.get(ConfigKey.MOVE_UP, arcade.key.W)):
            move_y += 1
        if self.input.is_pressed(Config.get(ConfigKey.MOVE_DOWN, arcade.key.S)):
            move_y -= 1
        if self.input.is_pressed(Config.get(ConfigKey.MOVE_LEFT, arcade.key.A)):
            move_x -= 1
        if self.input.is_pressed(Config.get(ConfigKey.MOVE_RIGHT, arcade.key.D)):
            move_x += 1

        # Normalize movement to prevent faster diagonal movement.
        movement_length = math.hypot(move_x, move_y)
        if movement_length > 0:
            move_x /= movement_length
            move_y /= movement_length

        self.change_x = move_x * self.movement_speed
        self.change_y = move_y * self.movement_speed

        # Get mouse direction, towards which the player should look.
        mouse_x, mouse_y = self.input.mouse_position
        direction_x = mouse_x - self.center_x
        direction_y = mouse_y - self.center_y

        if direction_x != 0 or direction_y != 0:
            angle = math.degrees(math.atan2(direction_y, direction_x))
            # Keep one consistent sprite face as "front" while tracking the mouse.
            self.angle = -angle + self.look_offset

        super().update(delta_time, *args, **kwargs)
