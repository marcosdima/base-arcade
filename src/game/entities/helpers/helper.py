from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..entity import Entity


class Helper:
    def __init__(self, target: 'Entity'):
        self.target = target
        self.setup()


    def setup(self):
        pass
