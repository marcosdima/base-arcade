from typing import Literal

import arcade

from ..geometry import Point
from ..ui_element import UIElement, UIElementProps

AnchorY = Literal['center', 'top', 'bottom']
AnchorX = Literal['center', 'left', 'right']


class TextProps:
    def __init__(
        self,
        text: str,
        font_size: int = 14,
        font_color: tuple[int, int, int] = (0, 0, 0),
    ):
        self.text = text
        self.font_size = font_size
        self.font_color = font_color


class Text(UIElement):
    def __init__(
        self,
        props: UIElementProps,
        text_props: TextProps,
    ):
        props.debug = True
        super().__init__(props)

        self.content = text_props.text

        # Font properties.
        self.font_size = text_props.font_size
        self.font_color = text_props.font_color

        # Arcade text instance.
        self.__current_font = None
        self.__text_obj = None

    @property
    def text_size(self) -> Point:
        if self.__text_obj:
            return Point(self.__text_obj.content_width, self.__text_obj.content_height)
        else:
            # Estimate text size based on font size and character count.
            avg_char_width = (
                self.font_size * 0.6
            )  # Approximate average character width.
            width = avg_char_width * len(self.content)
            height = self.font_size
            return Point(width, height)

    def __create_text(
        self, anchor_x: AnchorX = 'center', anchor_y: AnchorY = 'center'
    ) -> arcade.Text:
        font = self.style.font
        if not font:
            raise ValueError('Font style must be defined for Text element.')

        if anchor_x == 'center':
            x = self.global_rect.center_x
        elif anchor_x == 'right':
            x = self.global_rect.right
        else:
            x = self.global_rect.left

        if anchor_y == 'center':
            y = self.global_rect.center_y
        elif anchor_y == 'top':
            y = self.global_rect.top
        else:
            y = self.global_rect.bottom

        text_obj = arcade.Text(
            self.content,
            x,
            y,
            font.color.as_tuple(),
            font.size,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )

        self.__current_font = font
        return text_obj

    def __update_text(self):
        font = self.style.font
        if not font:
            return

        if (
            not self.__current_font
            or font != self.__current_font
            or self.__text_obj.text != self.content
        ):
            self.__text_obj = self.__create_text()

    def draw(self):
        super().draw()
        self.__text_obj.draw()

    def update(self, dt):
        self.__update_text()
        super().update(dt)
