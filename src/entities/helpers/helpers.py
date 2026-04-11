from typing import TYPE_CHECKING
from .default import *


if TYPE_CHECKING:
    from ..entity import Entity


class Helpers:
    def __init__(self, owner: 'Entity'):
        self.owner = owner
        self._set_default_helpers()


    def _set_default_helpers(self):
        self.movement = Movement(self.owner)