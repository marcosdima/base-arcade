from __future__ import annotations

from dataclasses import dataclass

from .color import Color


def lerp(a: float, b: float, t: float) -> float:
    return a + ((b - a) * t)


type Value = float | Color


@dataclass
class AnimationValue:
    duration: float = 1.0  # Time to reach target in seconds.
    speed: float = 12.0  # Higher = faster response.
    initial_value: Value = 0.0
    target_value: Value = 0.0

    def __post_init__(self):
        self.__progress = 0.0
        self.__playing = False
        if type(self.initial_value) is not type(self.target_value):
            raise ValueError('Initial value and target value must be of the same type.')

    @property
    def value(self) -> Value:
        if not hasattr(self, 'initial_value') or not hasattr(self, 'target_value'):
            raise ValueError(
                'AnimatedValue must be started with initial and target values before accessing value.'
            )

        val, init, end = self.__progress, self.initial_value, self.target_value
        if isinstance(init, Color):
            r = int(lerp(init.r, end.r, val))
            g = int(lerp(init.g, end.g, val))
            b = int(lerp(init.b, end.b, val))
            a = int(lerp(init.a, end.a, val))
            return Color((r, g, b, a))
        elif isinstance(init, float):
            val = lerp(init, end, val)
            return val if val < 0.9 else 1
        else:
            raise TypeError('Unsupported value type for animation.')

    def start(self):
        self.__progress = 0.0
        self.__playing = True

    def update(self, dt: float):
        if not self.__playing:
            return

        if self.duration <= 0.0:
            self.__progress = 1.0
        else:
            step = (self.speed * dt) / self.duration
            self.__progress = min(1.0, self.__progress + step)

        if self.__progress >= 1.0:
            self.__playing = False

    def is_playing(self) -> bool:
        return self.__playing
