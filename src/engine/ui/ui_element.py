from ..input import MouseButton
from .geometry import Point, Rect


class UIElementProps:
    def __init__(
        self,
        rect: Rect | tuple[float, float, float, float] = (0, 0, 0, 0),
        z_index: int = 0,
        name: str | None = None,
    ):
        if isinstance(rect, Rect):
            self.rect = rect
        else:
            x, y, width, height = rect
            self.rect = Rect(Point(x, y), width, height)
        self.z_index = z_index
        self.name = name


class UIElement:
    __count = 0

    def __init__(
        self,
        props: UIElementProps,
    ):
        # Unique ID for debugging and tracking.
        self.id = UIElement.__count
        UIElement.__count += 1

        # Base attributes.
        self.rect = props.rect
        self.z_index = props.z_index
        self.name = (
            props.name
            if props.name is not None
            else f'{self.__class__.__name__}_{self.id}'
        )
        self.str = 'A'

        # Parent-child relationship.
        self.parent: UIElement | None = None
        self.children: list[UIElement] = []

        # Flags.
        self.__disabled = False
        self.__visible = True
        self._mouse_over = False

    @property
    def position(self) -> Point:
        return self.rect.point - (self.rect.width / 2, self.rect.height / 2)

    @property
    def global_position(self) -> Point:
        if self.parent:
            return self.parent.global_position + self.position
        return self.rect.point

    @property
    def global_rect(self) -> Rect:
        return Rect(self.global_position, self.rect.width, self.rect.height)

    @property
    def global_z_index(self) -> int:
        if self.parent:
            return self.parent.global_z_index + self.z_index
        return self.z_index

    @property
    def is_visible(self) -> bool:
        if self.parent and not self.parent.is_visible:
            return False
        return self.__visible

    @property
    def is_disabled(self) -> bool:
        if self.parent and self.parent.is_disabled():
            return True
        return self.__disabled

    def change_visibility(self, visible: bool):
        self.__visible = visible

    def change_disabled(self, disabled: bool):
        self.__disabled = disabled

    def contains(self, global_point: Point | tuple) -> bool:
        if not self.parent:
            return self.rect.contains(global_point)
        return self.global_rect.contains(global_point)

    """ --- Parent-child relationship --- """

    def add_child(self, child: 'UIElement'):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: 'UIElement'):
        if child in self.children:
            child.parent = None
            self.children.remove(child)
        else:
            raise ValueError(f"Child {child} not found in {self.name}'s children.")

    """ --- Core methods --- """

    def draw(self):
        if not self.is_visible:
            return

        for child in self.children:
            child.draw()

    def update(self, dt: float):
        self.__propagate_event('on_update', dt)

    """ --- Input event handlers --- """

    def receive_mouse_motion(self, x, y, dx, dy) -> bool:
        p = Point(x, y)
        dp = Point(dx, dy)

        # If element does not contain the mouse position, the omit it.
        if not self.contains(p):
            if self._mouse_over:
                self._mouse_over = False

                # Captured by itself.
                if not self._on_mouse_out(p):
                    return self.__propagate_event('receive_mouse_motion', x, y, dx, dy)
            return False

        # If contains it and _mouse_over is False, trigger on_mouse_in.
        elif not self._mouse_over:
            self._mouse_over = True
            if not self._on_mouse_in(p):
                return self.__propagate_event('receive_mouse_motion', x, y, dx, dy)

        # Trigger on_mouse_over if the mouse is still over the element.
        if not self._on_mouse_over(p, dp):
            return self.__propagate_event('receive_mouse_motion', x, y, dx, dy)

    def receive_mouse_press(self, x, y, button: MouseButton, modifiers) -> bool:
        p = Point(x, y)

        # If element is disabled or not under mouse, do nothing.
        if self.__disabled or not self._mouse_over:
            return False

        return self._on_mouse_press(p, button, modifiers)

    def receive_mouse_release(self, x, y, button: MouseButton, modifiers) -> bool:
        p = Point(x, y)

        # If element is disabled or not under mouse, do nothing.
        if self.__disabled or not self._mouse_over:
            return False

        return self._on_mouse_release(p, button, modifiers)

    def receive_mouse_scroll(self, x, y, scroll_x: int, scroll_y: int) -> bool:
        p = Point(x, y)

        # If element is disabled or not under mouse, do nothing.
        if self.__disabled or not self._mouse_over:
            return False

        return self._on_mouse_scroll(p, scroll_x, scroll_y)

    def __propagate_event(self, event_name: str, *args, **kwargs) -> bool:
        # Propagate to children (last in, first out).
        for child in reversed(self.children):
            handler = getattr(child, event_name, None)

            if handler is None:
                raise AttributeError(
                    f"Event handler '{event_name}' not found in {self.__class__.__name__}."
                )

            was_consumed = handler(*args, **kwargs)
            if was_consumed:
                return True

        return False

    """ --- Mouse event protected methods --- """

    def _on_mouse_over(self, p: Point, dp: Point) -> bool:  # noqa: ARG002
        return False

    def _on_mouse_in(self, p: Point) -> bool:  # noqa: ARG002
        return False

    def _on_mouse_out(self, p: Point) -> bool:  # noqa: ARG002
        return False

    def _on_mouse_press(self, p: Point, button: MouseButton, modifiers) -> bool:  # noqa: ARG002
        return False

    def _on_mouse_release(self, p: Point, button: MouseButton, modifiers) -> bool:  # noqa: ARG002
        return False

    def _on_mouse_scroll(self, p: Point, scroll_x: int, scroll_y: int) -> bool:  # noqa: ARG002
        return False
