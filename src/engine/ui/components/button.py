import arcade

from ...input import MouseButton
from ..geometry import Point
from ..ui_element import UIElement, UIElementProps
from .text import Text, TextProps


class ButtonProps:
    def __init__(
        self,
        text: str,
        on_click: callable = lambda: None,
        style: dict | None = None,  # Placeholder for future styling options.
    ):
        self.text = text
        self.on_click = on_click
        self.style = style


class Button(UIElement):
    def __init__(self, props: UIElementProps, button_props: ButtonProps):
        super().__init__(props)

        self.label = button_props.text
        self.on_click = button_props.on_click
        self.style = button_props.style  # lo dejamos opcional por ahora

        self.__clicked_on = False

        self.text = Text(
            props=UIElementProps(rect=self.rect.clone()),
            text_props=TextProps(
                text=button_props.text, font_color=arcade.color.WHITE, font_size=14
            ),
        )
        self.add_child(self.text)

    """ --- Core methods --- """

    def draw(self):
        color = arcade.color.RED

        if self.__clicked_on:
            color = arcade.color.DARK_GRAY
        elif self._mouse_over:
            color = arcade.color.LIGHT_GRAY

        arcade.draw_rect_filled(
            rect=self.rect.as_arcade_rect(),
            color=color,
            tilt_angle=0,  # No rotation for now.
        )
        super().draw()

    """ --- Mouse event handlers --- """

    def _on_mouse_press(self, p: Point, button: MouseButton, modifiers) -> bool:
        if button == MouseButton.LEFT:
            self.__clicked_on = True
            return True
        return False

    def _on_mouse_release(self, p: Point, button: MouseButton, modifiers):
        if button == MouseButton.LEFT:
            if self.__clicked_on:
                self.__clicked_on = False
                if self.on_click:
                    self.on_click()
            return True
        return False
