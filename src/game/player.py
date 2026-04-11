import arcade
import math
from ..handlers import MouseHandler, KeyboardHandler
from ..utils import Config, ConfigKey
from .entities import Entity


class Player: 
    def __init__(self, mouse: MouseHandler, keyboard: KeyboardHandler):
        # Handler references.
        self.mouse = mouse
        self.keyboard = keyboard

        # Player attributes.
        self.movement_speed = 5
        self.look_offset = -90

        # Entity body.
        self.body = Entity('PlayerBody', (100, 100))
        self.keyboard.on_key_pressed.subscribe(self._on_key_pressed)
        self.keyboard.on_key_released.subscribe(self._on_key_released)
        self.mouse.on_mouse_motion.subscribe(self._on_mouse_motion)

    
    def _on_key_pressed(self, key: int):
        self._update_movement()


    def _on_key_released(self, key: int):
        self._update_movement()


    def _update_movement(self):
        # Get key codes for movement keys from config. TODO: Config event changes to update these dynamically.
        move_up = Config.get(ConfigKey.MOVE_UP, arcade.key.W)
        move_down = Config.get(ConfigKey.MOVE_DOWN, arcade.key.S)
        move_left = Config.get(ConfigKey.MOVE_LEFT, arcade.key.A)
        move_right = Config.get(ConfigKey.MOVE_RIGHT, arcade.key.D)

        # Check if the pressed key is one of the movement keys and update movement accordingly.
        move_x, move_y = (0, 0)
        if self.keyboard.is_pressed(move_up):
            move_y += 1
        if self.keyboard.is_pressed(move_down):
            move_y -= 1
        if self.keyboard.is_pressed(move_left):
            move_x -= 1
        if self.keyboard.is_pressed(move_right):
            move_x += 1

        self.body.helpers.movement.move((move_x, move_y), self.movement_speed)


    def _on_mouse_motion(self, mouse_x: int, mouse_y: int, _dx: int, _dy: int):
        # Get mouse direction, towards which the player should look.
        direction_x = mouse_x - self.body.center_x
        direction_y = mouse_y - self.body.center_y

        if direction_x != 0 or direction_y != 0:
            angle = math.degrees(math.atan2(direction_y, direction_x))
            # Keep one consistent sprite face as "front" while tracking the mouse.
            self.body.angle = -angle + self.look_offset
