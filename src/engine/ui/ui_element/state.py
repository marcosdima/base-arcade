from enum import IntEnum
from typing import TYPE_CHECKING

from ..style import Style

if TYPE_CHECKING:
    from .ui_element import UIElement


class UIStateValue(IntEnum):
    ACTIVE = 1
    DISABLED = 2
    HOVER = 3
    FOCUS = 4
    CLICKED = 5


class UIState:
    def __init__(self, owner: 'UIElement'):
        self.owner = owner

        self.__styles: dict[UIStateValue, Style] = {}

        # State attributes.
        self.focus: bool = False
        self.clicked_on: bool = False
        self.mouse_over: bool = False
        self.disabled: bool = False
        self.visible: bool = True
        self.current_state: UIStateValue = UIStateValue.ACTIVE

    @property
    def state_style(self) -> Style:
        return self.__styles.get(self.current_state, self.active_style)

    @property
    def active_style(self) -> Style:
        return self.__styles.get(UIStateValue.ACTIVE, Style())

    def change_state(self, new_state: UIStateValue):
        self.current_state = new_state
        self.owner.animations.transition_to(
            self.state_style,
        )

    def change_state_style(self, state: UIStateValue, style: Style):
        self.__styles[state] = style

    def disable(self):
        self.disabled = True
        self.change_state(UIStateValue.DISABLED)

    def enable(self):
        self.disabled = False
        if self.mouse_over:
            self.change_state(UIStateValue.HOVER)
        else:
            self.change_state(UIStateValue.ACTIVE)

    def set_mouse_over(self, value: bool):
        self.mouse_over = value
        if not self.disabled and self.mouse_over:
            self.change_state(UIStateValue.HOVER)
        elif not self.disabled:
            self.change_state(UIStateValue.ACTIVE)

    def set_clicked_on(self, value: bool):
        # Update attribute.
        self.clicked_on = value

        # Don't change state if disabled.
        if self.current_state == UIStateValue.DISABLED:
            return

        if self.clicked_on:
            self.change_state(UIStateValue.CLICKED)
        elif self.mouse_over:
            self.change_state(UIStateValue.HOVER)
        else:
            self.change_state(UIStateValue.ACTIVE)
