import math

import arcade

from ..helper import Helper


class Hitbox(Helper):
    def set_square(self, size: tuple[int]):
        width, height = size
        half_width = width / 2
        half_height = height / 2

        self.target.hit_box = arcade.hitbox.HitBox(
            [
                (-half_width, -half_height),
                (half_width, -half_height),
                (half_width, half_height),
                (-half_width, half_height),
            ]
        )

    def set_triangle(self, size: tuple[int]):
        width, height = size
        half_width = width / 2
        half_height = height / 2

        self.target.hit_box = arcade.hitbox.HitBox(
            [
                (0, half_height),
                (half_width, -half_height),
                (-half_width, -half_height),
            ]
        )

    def set_circle(self, radius: float, segments: int = 16):
        if segments < 3:
            raise ValueError('segments must be >= 3')

        points = []

        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            points.append((x, y))

        self.target.hit_box = arcade.hitbox.HitBox(points)
