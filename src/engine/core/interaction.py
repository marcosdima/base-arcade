from collections.abc import Callable


class Interaction:
    def __init__(
        self,
        name: str,
        action: Callable[[], None],
        priority: int = 0,
        on_focus: Callable[[], None] | None = None,
        on_blur: Callable[[], None] | None = None,
    ):
        self.name = name
        self.action = action
        self.priority = priority

        self.on_focus = on_focus
        self.on_blur = on_blur

    def execute(self):
        self.action()

    def focus(self):
        if self.on_focus:
            self.on_focus()

    def blur(self):
        if self.on_blur:
            self.on_blur()
