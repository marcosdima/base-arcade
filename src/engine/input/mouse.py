from ..core import Event
from .mouse_button import MouseButton


class MouseHandler:
    def __init__(self):
        self.position: tuple[int, int] = (0, 0)
        self.delta: tuple[int, int] = (0, 0)

        # Events.
        self.on_mouse_motion = Event[[int, int, int, int]]()
        self.on_left_click = Event[[int, int]]()
        self.on_right_click = Event[[int, int]]()
        self.on_middle_click = Event[[int, int]]()
        self.on_roll_up = Event[[int, int]]()
        self.on_roll_down = Event[[int, int]]()

    def update_mouse(self, x: int, y: int, dx: int, dy: int):
        self.position = (x, y)
        self.delta = (dx, dy)
        self.on_mouse_motion.trigger(x, y, dx, dy)

    def receive_mouse_release(self, x: int, y: int, button: int):
        if button == MouseButton.LEFT:
            self.on_left_click.trigger(x, y)
        elif button == MouseButton.RIGHT:
            self.on_right_click.trigger(x, y)
        elif button == MouseButton.MIDDLE:
            self.on_middle_click.trigger(x, y)

    def receive_mouse_press(self, x: int, y: int, button: int):
        if button == MouseButton.LEFT:
            self.on_left_click.trigger(x, y)
        elif button == MouseButton.RIGHT:
            self.on_right_click.trigger(x, y)
        elif button == MouseButton.MIDDLE:
            self.on_middle_click.trigger(x, y)
