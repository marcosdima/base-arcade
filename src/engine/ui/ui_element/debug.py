from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import UIElement


class Debug:
    def __init__(self, owner: 'UIElement', enabled: bool = False):
        self.enabled = enabled
        self.owner = owner
        self.__time_acc = 0.0

    def print(self, title: str, message: str):
        if self.enabled:
            print(f'\t [DEBUG] {title} {message}')

    def show(self, time_acc: float):
        if self.enabled and self.__time_acc == 0:
            print('----------------------------------------')
            print(f'[DEBUG] Name: {self.owner.name} - Visible: {self.owner.is_visible}')
            print(
                f'[DEBUG] Rect: {self.owner.rect} - Global Rect: {self.owner.global_rect}'
            )
            print(f'[DEBUG] Style - BG: {self.owner.style.background_color}')
            print('----------------------------------------')

        self.__time_acc += time_acc
        if self.__time_acc >= 5.0:
            self.__time_acc = 0
