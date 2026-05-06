from dataclasses import dataclass, field
from enum import IntEnum

from ..style import Style


class UIStateValue(IntEnum):
    ACTIVE = 1
    DISABLED = 2
    HOVER = 3
    FOCUS = 4
    CLICKED = 5


@dataclass
class UIState:
    focus: bool = False
    clicked_on: bool = False
    mouse_over: bool = False
    disabled: bool = False
    visible: bool = True
    current: UIStateValue = UIStateValue.ACTIVE
    styles: dict[UIStateValue, Style] = field(default_factory=dict)

    @property
    def style(self) -> Style:
        if self.current in self.styles:
            return self.styles[self.current]
        return self.styles.get(UIStateValue.ACTIVE, Style())

    def change_state(self, new_state: UIStateValue):
        self.current = new_state

    def save_style(self, style: Style, state: UIStateValue = UIStateValue.ACTIVE):
        self.styles[state] = style

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
        if self.current == UIStateValue.DISABLED:
            return

        if self.clicked_on:
            self.change_state(UIStateValue.CLICKED)
        elif self.mouse_over:
            self.change_state(UIStateValue.HOVER)
        else:
            self.change_state(UIStateValue.ACTIVE)
