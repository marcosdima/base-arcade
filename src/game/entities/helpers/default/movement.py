import math
from arcade import PymunkPhysicsEngine
from ..helper import Helper


class Movement(Helper):
    def setup(self):
        self.physics: PymunkPhysicsEngine = None
        self.speed: float = 10.0


    def move(self, direction: tuple[float, float], intensity: float = 100.0):
        dx, dy = direction

        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        vx = dx * (self.speed / 100 * intensity)
        vy = dy * (self.speed / 100 * intensity)

        if self.physics:
            self.physics.set_velocity(self.target, (vx, vy))
        else:
            self.target.change_x = vx
            self.target.change_y = vy


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


