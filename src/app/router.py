from ..engine import BaseView

type ViewFactory = callable[[], BaseView]


class Router:
    def __init__(
        self,
        window,
        routes: dict[str, ViewFactory],
        initial: str,
    ):
        """
        Args:
            window: The arcade.Window instance.
            routes: A dictionary mapping route names to view factory functions.
            initial: The initial route name.
        """
        self.window = window
        self.routes = routes

        self._stack = []
        self._current_name = None

        self.navigate(initial)

    def _create_view(self, name: str):
        if name not in self.routes:
            raise ValueError(f"Route '{name}' not found")

        factory = self.routes[name]
        view = factory()

        # TODO: This is a bit hacky, but it allows us to inject the router into views that need it without forcing all views to have a router attribute passed in the constructor. We can improve this later by using a more robust dependency injection system.
        if hasattr(view, 'router'):
            view.router = self

        return view

    def navigate(self, name: str):
        view = self._create_view(name)

        self._stack.append(view)
        self._current_name = name

        self.window.show_view(view)

    def go_back(self):
        if len(self._stack) <= 1:
            return

        self._stack.pop()
        previous = self._stack[-1]
        self.window.show_view(previous)

    def reset(self, name: str):
        """Clear stack and go to view"""
        while self._stack:
            self._stack.pop()

        self.navigate(name)
