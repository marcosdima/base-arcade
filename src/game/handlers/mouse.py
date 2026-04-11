from ...utils import Event


class MouseHandler:
	def __init__(self):
		self.position: tuple[int, int] = (0, 0)
		self.delta: tuple[int, int] = (0, 0)
		self.on_mouse_motion = Event[[int, int, int, int]]()


	def update_mouse(self, x: int, y: int, dx: int, dy: int):
		self.position = (x, y)
		self.delta = (dx, dy)
		self.on_mouse_motion.trigger(x, y, dx, dy)
