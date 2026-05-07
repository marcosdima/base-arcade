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

        self.__clicked_on = False

        self.text = Text(
            props=UIElementProps(rect=self.rect.just_size()),
            text_props=TextProps(
                text=button_props.text, font_color=arcade.color.WHITE, font_size=14
            ),
        )
        self.add_child(self.text)

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

    def _on_mouse_in(self, p):
        self.style.background_color = 'dark_blue'

    def _on_mouse_out(self, p):
        self.style.background_color = 'gray'
