from ..utils import Event


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
