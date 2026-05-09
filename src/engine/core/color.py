from dataclasses import dataclass
from typing import Literal

from arcade.color import Color as ArcadeColor

ColorString = Literal[
    'red',
    'green',
    'blue',
    'black',
    'white',
    'light_gray',
    'dark_gray',
    'yellow',
    'cyan',
    'magenta',
    'orange',
    'purple',
    'brown',
    'pink',
    'gray',
    'light_blue',
    'dark_blue',
    'light_green',
    'dark_green',
    'light_red',
    'dark_red',
    'transparent',
]

type ColorValue = tuple[int, int, int, int]
type ColorProp = ColorString | ColorValue

COLOR_MAP: dict[ColorString, ColorValue] = {
    'red': (255, 0, 0, 255),
    'green': (0, 255, 0, 255),
    'blue': (0, 0, 255, 255),
    'black': (0, 0, 0, 255),
    'white': (255, 255, 255, 255),
    'light_gray': (211, 211, 211, 255),
    'dark_gray': (169, 169, 169, 255),
    'yellow': (255, 255, 0, 255),
    'cyan': (0, 255, 255, 255),
    'magenta': (255, 0, 255, 255),
    'orange': (255, 165, 0, 255),
    'purple': (128, 0, 128, 255),
    'brown': (165, 42, 42, 255),
    'pink': (255, 192, 203, 255),
    'gray': (128, 128, 128, 255),
    'light_blue': (173, 216, 230, 255),
    'dark_blue': (0, 0, 139, 255),
    'light_green': (144, 238, 144, 255),
    'dark_green': (0, 100, 0, 255),
    'light_red': (255, 102, 102, 255),
    'dark_red': (139, 0, 0, 255),
    'transparent': (0, 0, 0, 0),
}


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def __init__(self, value: ColorProp):
        r, g, b, a = self.__validate_prop(value)
        self.r, self.g, self.b, self.a = r, g, b, a

    def __validate_prop(self, value: ColorProp) -> ColorValue:
        # Validate that the string is a valid color name.
        if isinstance(value, str):
            if value not in COLOR_MAP:
                raise ValueError(f'Invalid color name: {value}')
            return COLOR_MAP[value]
        # Validate that the tuple is either RGB or RGBA and that all components are in the range 0-255.
        elif isinstance(value, tuple):
            if len(value) == 3:
                r, g, b = value
                a = 255
            elif len(value) >= 4:
                r, g, b, a = value
            else:
                raise ValueError('Color tuple must have 3 (RGB) or 4 (RGBA) values.')
            for component in (r, g, b, a):
                if not (0 <= component <= 255):
                    raise ValueError('Color components must be in the range 0-255.')
            return (r, g, b, a)
        # If it's neither a string nor a tuple, it's an invalid type.
        else:
            raise TypeError(
                f'Color value must be a ColorString or a tuple. Received: {value}'
            )

    def as_tuple(self) -> ColorValue:
        return (self.r, self.g, self.b, self.a)

    def darker(self, factor: int = 1, magnitude: float = 0.1) -> 'Color':
        return self.copy(factor=1 - (factor * magnitude))

    def lighter(self, factor: int = 1, magnitude: float = 0.1) -> 'Color':
        return self.copy(factor=1 + (factor * magnitude))

    def copy(self, factor: float = 1.0) -> 'Color':
        return Color(
            (
                min(int(self.r * factor), 255),
                min(int(self.g * factor), 255),
                min(int(self.b * factor), 255),
                self.a,
            )
        )

    def __eq__(self, value):
        if isinstance(value, Color):
            return self.as_tuple() == value.as_tuple()
        elif isinstance(value, ArcadeColor):
            return self.as_tuple() == (value.r, value.g, value.b, value.a)
        else:
            return False
