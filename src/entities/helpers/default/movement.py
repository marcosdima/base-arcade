import math
from ..helper import Helper


class Movement(Helper):
    def move(self, direction: tuple[float, float], speed: float):
        dir_x, dir_y = direction
        
        # Normalize movement to prevent faster diagonal movement.
        move_x, move_y = direction
        movement_length = math.hypot(move_x, move_y)
        if movement_length > 0:
            move_x /= movement_length
            move_y /= movement_length
        
        self.target.change_x = move_x * speed
        self.target.change_y = move_y * speed