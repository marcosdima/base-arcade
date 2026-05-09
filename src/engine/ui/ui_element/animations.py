from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from ...core import AnimationValue
from ..style import Style

if TYPE_CHECKING:
    from .ui_element import UIElement


class AnimableProperty(Enum):
    BACKGROUND_COLOR = 'background_color'
    BORDER = 'border'
    FONT = 'font'


class Animations:
    def __init__(self, owner: UIElement):
        self.owner = owner
        self.active: dict[AnimableProperty, AnimationValue] = {}

    def transition_to(self, target: Style):
        current = self.owner.computed_style

        if target.is_set(target.background_color):
            current_value = current.background_color
            target_value = target.background_color

            if current_value != target_value:
                animation = AnimationValue(
                    duration=0.2,
                    speed=0.2,
                    initial_value=current_value,
                    target_value=target_value,
                )

                self.__interrupt_animation(
                    AnimableProperty.BACKGROUND_COLOR,
                    animation,
                )

        if target.is_set(target.font):
            current_value = current.font.color
            target_value = target.font.color

            if current_value != target_value:
                animation = AnimationValue(
                    duration=0.2,
                    speed=0.2,
                    initial_value=current_value,
                    target_value=target_value,
                )

                self.__interrupt_animation(
                    AnimableProperty.FONT,
                    animation,
                )

        if target.is_set(target.border):
            current_value = current.border.color
            target_value = target.border.color
            if current_value != target_value:
                animation = AnimationValue(
                    duration=0.2,
                    speed=0.2,
                    initial_value=current_value,
                    target_value=target_value,
                )

                self.__interrupt_animation(
                    AnimableProperty.BORDER,
                    animation,
                )

    def update(self, dt: float):
        ended = set()

        for prop, animation in self.active.items():
            animation.update(dt)

            value = animation.value

            match prop:
                case AnimableProperty.BACKGROUND_COLOR:
                    self.owner.computed_style.background_color = value
                case AnimableProperty.FONT:
                    self.owner.computed_style.font.color = value
                case AnimableProperty.BORDER:
                    self.owner.computed_style.border.color = value

            if not animation.is_playing():
                ended.add(prop)

        for prop in ended:
            del self.active[prop]

    def __interrupt_animation(self, prop: AnimableProperty, new_value: AnimationValue):
        if self.active.get(prop, None) is not None:
            current_animation = self.active[prop]
            new_value.start_value = current_animation.value
        self.active[prop] = new_value
        new_value.start()
