from dataclasses import dataclass
from typing import Literal

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
        r, g, b, a = (
            # If it's a string, look it up in the color map.
            COLOR_MAP[value]
            if isinstance(value, str)
            # If it's a tuple and has at least 4 values, use the first 4 as RGBA.
            else value
            if len(value) >= 4
            # If it's a tuple with 3 values, use those as RGB and default alpha to 255.
            else (*value, 255)
        )
        self.r, self.g, self.b, self.a = r, g, b, a

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
