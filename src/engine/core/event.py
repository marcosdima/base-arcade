from collections.abc import Callable
from typing import ParamSpec

P = ParamSpec('P')


class Callback:
    def __init__(self, fn: Callable[P, None], priority: int = 0):
        self.fn = fn
        self.priority = priority


class Event[**P]:
    def __init__(self, validators: set[Callable[P, bool]] = None) -> None:
        # Set of callback functions that will be called when the event is triggered.
        self.callbacks: set[Callback] = set()
        self.__sorted_callbacks: list[Callback] = []

        # Optional list of validator functions that will be called before triggering the event.
        self.validators = validators if validators is not None else set()

    def subscribe(self, fn: Callable[P, None], priority: int = 0) -> None:
        """
        Subscribe a callback function to the event. The function will be called when the event is triggered.
        Args:
            fn: The callback function to subscribe. It should accept the same parameters as the event.
            priority: The priority of the callback function. Higher priority functions will be called first.
        """
        if self.has(fn):
            raise ValueError('Callback already subscribed')

        self.callbacks.add(Callback(fn, priority))
        self.__sorted_callbacks = sorted(
            self.callbacks, key=lambda cb: cb.priority, reverse=True
        )

    def unsubscribe(self, fn: Callable[P, None]) -> None:
        """
        Unsubscribe a callback function from the event.
        Args:
            fn: The callback function to remove from callbacks.
        Raises:
            ValueError: If the callback function is not found in the list of subscribed callbacks.
        """
        cb = next((cb for cb in self.callbacks if cb.fn == fn), None)
        if not self.has(fn):
            raise ValueError('Callback not found')
        self.callbacks = self.callbacks - {cb}
        self.__sorted_callbacks = sorted(
            self.callbacks, key=lambda cb: cb.priority, reverse=True
        )

    def trigger(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Trigger the event, calling all subscribed callback functions with the provided arguments.
        Args:
            *args: Positional arguments to pass to the callback functions.
            **kwargs: Keyword arguments to pass to the callback functions.
        Raises:
            ValueError: If any of the validators fail (return False) when called with the provided arguments.
        """
        if not all(v(*args, **kwargs) for v in self.validators):
            raise ValueError('Event validation failed')

        for cb in self.__sorted_callbacks:
            cb.fn(*args, **kwargs)

    def clear(self) -> None:
        """Clear all subscribed callback functions from the event."""
        self.callbacks.clear()
        self.__sorted_callbacks.clear()

    def has(self, fn: Callable[P, None]) -> bool:
        """Check if a callback function is subscribed to the event."""
        return any(cb.fn == fn for cb in self.callbacks)
