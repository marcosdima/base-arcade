from arcade import View, color
from ..handlers import MouseHandler, KeyboardHandler

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
        pass


    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        # Called when a mouse button is released.
        pass

    
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # Called when the mouse moves.
        self.mouse_handler.update_mouse(x, y, dx, dy)