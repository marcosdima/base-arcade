class Point:
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
    ):
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Point':
        # Point + Point.
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        # Point + (x, y).
        elif isinstance(other, tuple):
            parsed = Point.parse_from_tuple(other)
            if parsed is not NotImplemented:
                return self + parsed
        return NotImplemented

    @classmethod
    def parse_from_tuple(cls, data: tuple) -> 'Point':
        if len(data) >= 2:
            x, y = data[0], data[1]
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                return cls(x, y)
        raise ValueError(
            'Invalid tuple for Point parsing. Expected a tuple with at least two numeric values.'
        )


class Rect:
    def __init__(self, point: Point = Point(), width: float = 0, height: float = 0):
        self.point = point
        self.width = width
        self.height = height

    @property
    def x(self) -> float:
        return self.point.x

    @property
    def y(self) -> float:
        return self.point.y

    @property
    def center(self) -> Point:
        return Point(self.center_x, self.center_y)

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2

    def contains(self, point: Point | tuple) -> bool:
        if isinstance(point, Point):
            return (self.x <= point.x <= self.x + self.width) and (
                self.y <= point.y <= self.y + self.height
            )
        elif isinstance(point, tuple) and len(point) >= 2:
            a, b = point[0], point[1]
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return (self.x <= a <= self.x + self.width) and (
                    self.y <= b <= self.y + self.height
                )
        return NotImplemented
