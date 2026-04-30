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
        self.__text_obj = arcade.Text(
            self.content,
            0,
            0,
            arcade.color.BLACK,
            14,
            anchor_x='left',
            anchor_y='bottom',
        )

    def __update_text(self):
        self.__text_obj.text = self.content
        self.__text_obj.x = self.rect.x
        self.__text_obj.y = self.rect.y

    def draw(self):
        self.__update_text()
        self.__text_obj.draw()
        return super().draw()
