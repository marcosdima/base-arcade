import arcade
from enum import Enum


class MouseButton(Enum):
    LEFT = arcade.mouse.LEFT
    RIGHT = arcade.mouse.RIGHT
    MIDDLE = arcade.mouse.MIDDLE
    BUTTON_4 = arcade.mouse.BUTTON_4
    BUTTON_5 = arcade.mouse.BUTTON_5