import math
from arcade import PymunkPhysicsEngine
from ..helper import Helper


class Movement(Helper):
    def setup(self):
        self.physics: PymunkPhysicsEngine = None


    def move(self, direction: tuple[float, float], speed: float):
        # Check if physics is available. If not, use simple movement.
        if not self.physics:
            self._move_with_no_physics(direction, speed)
            return
        
        dx, dy = direction

        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        vx = dx * speed
        vy = dy * speed

        self.physics.set_velocity(self.target, (vx, vy))


    def rotate(self, angle: float):
        if self.physics:
            self.physics.set_rotation(self.target, -angle)
        else:
            self.target.angle = angle


    def _move_with_no_physics(self, direction: tuple[float, float], speed: float):
        # Normalize movement to prevent faster diagonal movement.
        move_x, move_y = direction
        movement_length = math.hypot(move_x, move_y)
        if movement_length > 0:
            move_x /= movement_length
            move_y /= movement_length
        
        self.target.change_x = move_x * speed
        self.target.change_y = move_y * speed