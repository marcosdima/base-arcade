from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import UIElement


class Debug:
    def __init__(self, owner: 'UIElement', enabled: bool = False):
        self.enabled = enabled
        self.owner = owner

    def print(self, title: str, message: str):
        if self.enabled:
            print(f'\t [DEBUG] {title} {message}')
