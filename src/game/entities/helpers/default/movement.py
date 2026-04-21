import math
from arcade import PymunkPhysicsEngine
from ..helper import Helper


class Movement(Helper):
    def setup(self):
        self.physics: PymunkPhysicsEngine = None
        self.speed: float = 10.0


    def move(self, direction: tuple[float, float]):
        # Check if physics is available. If not, use simple movement.
        if not self.physics:
            self._move_with_no_physics(direction)
            return
        
        dx, dy = direction

        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        vx = dx * self.speed
        vy = dy * self.speed

        self.physics.set_velocity(self.target, (vx, vy))


    def rotate(self, angle: float):
        if self.physics:
            self.physics.set_rotation(self.target, -angle)
        else:
            self.target.angle = angle


    def stop(self):
        if self.physics:
            self.physics.set_velocity(self.target, (0, 0))
        else:
            self.target.change_x = 0
            self.target.change_y = 0


    def _move_with_no_physics(self, direction: tuple[float, float]):
        # Normalize movement to prevent faster diagonal movement.
        move_x, move_y = direction
        movement_length = math.hypot(move_x, move_y)
        if movement_length > 0:
            move_x /= movement_length
            move_y /= movement_length
        
        self.target.change_x = move_x * self.speed
        self.target.change_y = move_y * self.speed