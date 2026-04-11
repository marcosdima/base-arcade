import arcade
from pytiled_parser import Color
from ..utils import Event

class Area:
    def __init__(self, x, y, width, height):
        self.sprite = arcade.SpriteSolidColor(width, height, Color(0, 0, 0, 0))
        self.sprite.center_x = x + width / 2
        self.sprite.center_y = y + height / 2
        self.sprite.sync_hit_box_to_texture()

        self._inside = set()
        self.on_enter: Event = Event()
        self.on_exit: Event = Event()
        self.on_enter.subscribe(fn=lambda s: print(f"Sprite {s} entered area"))
        self.on_exit.subscribe(fn=lambda s: print(f"Sprite {s} exited area"))


    def update(self, sprites: list):
        current_inside = set()

        # Check for collisions with the area sprite and the provided sprites
        for s in sprites:
            if arcade.check_for_collision(s, self.sprite):
                current_inside.add(s)
                if s not in self._inside:
                    self.on_enter.trigger(s)

        # Check for sprites that were inside but are no longer inside
        for s in self._inside:
            if s not in current_inside:
                self.on_exit.trigger(s)

        # Update the inside set for the next update cycle.
        self._inside = current_inside