from ...input import MouseButton
from ..geometry import Point
from ..ui_element import UIElement, UIElementProps
from .text import Text, TextProps


class ButtonProps:
    def __init__(
        self,
        text: str,
        on_click: callable = lambda: None,
    ):
        self.text = text
        self.on_click = on_click


class Button(UIElement):
    def __init__(self, props: UIElementProps, button_props: ButtonProps):
        super().__init__(props)

        self.label = button_props.text
        self.on_click = button_props.on_click

        self.text = Text(
            props=UIElementProps(rect=self.rect.just_size()),
            text_props=TextProps(text=button_props.text),
        )
        self.add_child(self.text)

        self.events.on_mouse_release.subscribe(self.__on_mouse_release)

    def __on_mouse_release(self, p: Point, button: MouseButton, modifiers):
        if button == MouseButton.LEFT:
            self.on_click()
