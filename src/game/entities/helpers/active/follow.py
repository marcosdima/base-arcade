import math
from typing import TYPE_CHECKING
from ..helper import Helper


if TYPE_CHECKING:
    from ...entity import Entity


class Follow(Helper):
    def setup(self):
        self.follow_target: Entity | None = None
        self.follow_distance: float = 0.0
        self.target.on_update.subscribe(self._on_update)


    def _on_update(self, dt: float):
        # No target to follow, so do nothing.
        if self.follow_target is None:
            return

        # Measure the remaining distance to the target entity.
        delta_x = self.follow_target.center_x - self.target.center_x
        delta_y = self.follow_target.center_y - self.target.center_y
        distance = math.hypot(delta_x, delta_y)

        # Stay close enough to the target without overshooting it.
        step = self.target.helpers.movement.speed * dt
        if distance <= self.follow_distance:
            self.target.helpers.movement.stop()
            return

        if distance <= step + self.follow_distance:
            if self.follow_distance == 0:
                self.target.center_x = self.follow_target.center_x
                self.target.center_y = self.follow_target.center_y
            else:
                ratio = self.follow_distance / distance
                self.target.center_x = self.follow_target.center_x - delta_x * ratio
                self.target.center_y = self.follow_target.center_y - delta_y * ratio

            self.target.helpers.movement.stop()
            return

        self.target.helpers.movement.move((delta_x, delta_y))


    def follow(self, entity: 'Entity', distance: float = 0.0):
        self.follow_target = entity
        self.follow_distance = max(distance, 0.0)
