from geometry import Rect, Point
from ....engine import MouseButton


class UIElement:
    __count = 0

    def __init__(self, rect: Rect = Rect(), z_index: int = 0, name: str | None = None):
        self.rect = rect
        self.z_index = z_index
        self.name = name if name is not None else f"{self.__class__.__name__}_{self.id}"
        self.str = "A"

        # Parent-child relationship.
        self.parent: "UIElement" | None = None
        self.children: list["UIElement"] = []

        # Flags.
        self.visible = False
        self.disabled = False
        self.__mouse_over = False

        # Unique ID for debugging and tracking.
        self.id = UIElement.__count
        UIElement.__count += 1

    @property
    def global_position(self) -> Point:
        if self.parent:
            return self.parent.global_position + self.rect.point
        return self.rect.point

    def add_child(self, child: "UIElement"):
        child.set_parent(self)
        self.children.append(child)

    def change_visibility(self, visible: bool):
        self.visible = visible

    def contains(self, global_point: Rect | tuple) -> bool:
        if not self.parent:
            return self.rect.contains(global_point)
        offset_point = self.parent.global_position + self.rect.point
        offset_rect = Rect(offset_point, self.rect.width, self.rect.height)
        return offset_rect.contains(global_point)

    """ --- Core methods --- """

    def draw(self):
        if not self.visible:
            return

        for child in self.children:
            child.draw()

    def update(self, dt: float):
        self.__propagate_event("on_update", dt)

    """ --- Mouse event handlers --- """

    def on_mouse_over(self, p: Point, dp: Point):
        self.__propagate_event("on_mouse_in", p, dp)

    def on_mouse_in(self, p: Point):
        self.__mouse_over = True
        self.__propagate_event("on_mouse_over", p, Point(0, 0))

    def on_mouse_out(self, p: Point):
        self.__mouse_over = False
        self.__propagate_event("on_mouse_out", p)

    def on_mouse_press(self, p: Point, button: MouseButton, modifiers):
        self.__propagate_event("on_mouse_press", p, button, modifiers)

    def on_mouse_release(self, p: Point, button: MouseButton, modifiers):
        self.__propagate_event("on_mouse_release", p, button, modifiers)

    def __propagate_event(self, event_name: str, *args, **kwargs):
        handler = getattr(self, event_name, None)

        if callable(handler):
            handler(*args, **kwargs)
        else:
            raise AttributeError(
                f"Event handler '{event_name}' not found in {self.__class__.__name__}."
            )

        for child in self.children:
            child.__propagate_event(event_name, *args, **kwargs)
