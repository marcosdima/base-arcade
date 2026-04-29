import math

from ..helper import Helper


class Path(Helper):
    def setup(self):
        self.path_points: list[tuple[int, int]] = []
        self.path_to: tuple[int, int] | None = None
        self.target.on_update.subscribe(self._on_update)

    def _on_update(self, dt: float):
        # No path to follow, so do nothing.
        if self.path_to is None:
            return

        # Measure the remaining distance to the current waypoint.
        delta_x = self.path_to[0] - self.target.center_x
        delta_y = self.path_to[1] - self.target.center_y

        # Treat the waypoint as reached when the next step could overshoot it.
        step = self.target.helpers.movement.speed * dt
        if math.hypot(delta_x, delta_y) <= step:
            self.target.center_x = self.path_to[0]
            self.target.center_y = self.path_to[1]

            # No more points to follow, so clear the path.
            if not self.path_points:
                self.path_to = None
                self.target.helpers.movement.stop()
                return

            # Move to the next point in the path.
            self.path_to = self.path_points.pop(0)
            delta_x = self.path_to[0] - self.target.center_x
            delta_y = self.path_to[1] - self.target.center_y

        self.target.helpers.movement.move((delta_x, delta_y))

    def go_to(self, route: list[tuple[int, int]] | tuple[int, int]):
        # Clear any existing path points.
        self.path_points.clear()

        # Update the path_to attribute with the new destination coordinates.
        if isinstance(route, list):
            self.path_to = route[0]
            self.path_points = route[1:]
        else:
            self.path_to = route

        self.target.helpers.movement.move(self.path_to)
