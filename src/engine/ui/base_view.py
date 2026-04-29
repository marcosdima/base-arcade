import arcade
from arcade import View

from .. import KeyboardHandler, MouseHandler


class BaseView(View):
    def __init__(self):
        super().__init__()
        self.keyboard_handler = KeyboardHandler()
        self.mouse_handler = MouseHandler()

    def on_key_press(self, key: int, modifiers: int):
        # Called when a keyboard key is pressed.
        self.keyboard_handler.key_pressed(key)

    def on_key_release(self, key: int, modifiers: int):
        # Called when a keyboard key is released.
        self.keyboard_handler.key_released(key)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Called when a mouse button is pressed.
        if button == arcade.MOUSE_BUTTON_LEFT:  # Left click
            self.mouse_handler.on_left_click.trigger(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:  # Right click
            self.mouse_handler.on_right_click.trigger(x, y)
        elif button == arcade.MOUSE_BUTTON_MIDDLE:  # Middle click
            self.mouse_handler.on_middle_click.trigger(x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        # Called when a mouse button is released.
        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        # Called when the mouse wheel is scrolled.
        if scroll_y > 0:  # Scroll up
            self.mouse_handler.on_roll_up.trigger(x, y)
        elif scroll_y < 0:  # Scroll down
            self.mouse_handler.on_roll_down.trigger(x, y)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # Called when the mouse moves.
        self.mouse_handler.update_mouse(x, y, dx, dy)
