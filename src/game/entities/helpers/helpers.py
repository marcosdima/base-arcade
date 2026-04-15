from typing import TYPE_CHECKING

from .active import *
from .default import *


if TYPE_CHECKING:
    from ..entity import Entity


class Helpers:
    def __init__(self, owner: 'Entity'):
        self.owner = owner
        self._set_default_helpers()

        # Active helpers.
        self.interact: Interact = None


    def _set_default_helpers(self):
        self.movement = Movement(self.owner)


    def activate_intereaction(self):
        self.interact = Interact(self.owner)