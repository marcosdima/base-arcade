from arcade import View

from ..input import KeyboardHandler, MouseHandler
from .ui_element import UIElement, UIElementProps


class BaseView(View):
    def __init__(self):
        super().__init__()

        # Input handlers.
        self.keyboard_handler = KeyboardHandler()
        self.mouse_handler = MouseHandler()

        # Root ui element.
        ui_props = UIElementProps(
            rect=(0, 0, self.window.width, self.window.height),
            name='root',
        )
        self.root = UIElement(ui_props)

    def on_draw(self):
        self.root.draw()
        return super().on_draw()

    """ --- Arcade input event handlers --- """

    def on_key_press(self, key: int, modifiers: int):
        # Called when a keyboard key is pressed.
        self.keyboard_handler.key_pressed(key)

    def on_key_release(self, key: int, modifiers: int):
        # Called when a keyboard key is released.
        self.keyboard_handler.key_released(key)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Send event to mouse handler.
        self.mouse_handler.receive_mouse_press(x, y, button)

        # Call root to propagate the click to the UI.
        self.root.receive_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        # Send event to mouse handler.
        self.mouse_handler.receive_mouse_release(x, y, button)

        # Call root to propagate the click to the UI.
        self.root.receive_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        # Called when the mouse wheel is scrolled.
        if scroll_y > 0:  # Scroll up
            self.mouse_handler.on_roll_up.trigger(x, y)
        elif scroll_y < 0:  # Scroll down
            self.mouse_handler.on_roll_down.trigger(x, y)

        # Call root to propagate the scroll to the UI.
        self.root.receive_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        # Called when the mouse moves.
        self.mouse_handler.update_mouse(x, y, dx, dy)

        # Call root to propagate the motion to the UI.
        self.root.receive_mouse_motion(x, y, dx, dy)
