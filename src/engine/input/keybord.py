import arcade
from .. import Event

class KeyboardHandler:
	def __init__(self):
		self.keys: dict[int, bool] = {}

		# General events.
		self.on_key_pressed = Event[[int]]()
		self.on_key_released = Event[[int]]()

		# Indivudual key events.
		self.on_escape_pressed = Event()


	def key_pressed(self, key: int):
		self.keys[key] = True
		self.on_key_pressed.trigger(key)
		if key == arcade.key.ESCAPE:
			self.on_escape_pressed.trigger()
		

	def key_released(self, key: int):
		self.keys[key] = False
		self.on_key_released.trigger(key)


	def str_key_to_int(self, key_str: str) -> int | None:
		return getattr(arcade.key, key_str.upper(), None)


	def is_pressed(self, key: int | str) -> bool:
		resolved_key = self.str_key_to_int(key) if isinstance(key, str) else key
		return self.keys.get(resolved_key, False)
	
    
