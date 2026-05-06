import arcade

from ..ui_element import UIElement, UIElementProps


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
        super().__init__(props)

        self.content = text_props.text

        # Font properties.
        self.font_size = text_props.font_size
        self.font_color = text_props.font_color

        # Arcade text instance.
        self.__current_font = None
        self.__text_obj = None

    def __create_text(self) -> arcade.Text:
        font = self.style.font
        if not font:
            raise ValueError('Font style must be defined for Text element.')

        text_obj = arcade.Text(
            self.content,
            self.rect.x,
            self.rect.y,
            font.color.as_tuple(),
            font.size,
            anchor_x='left',
            anchor_y='bottom',
        )
        self.__current_font = font
        return text_obj

    def __update_text(self):
        font = self.style.font
        if not font:
            return

        if not self.__current_font or font != self.__current_font:
            self.__text_obj = self.__create_text()
        else:
            self.__text_obj.text = self.content
            self.__text_obj.x = self.rect.x
            self.__text_obj.y = self.rect.y

    def draw(self):
        self.__update_text()
        self.__text_obj.draw()
        return super().draw()
