from collections.abc import Callable
from typing import Generic, ParamSpec

P = ParamSpec('P')
Validator = Callable[..., bool]


class Event(Generic[P]):
    def __init__(self, validators: list[Validator] | None = None):
        # Set of callback functions that will be called when the event is triggered.
        self.callbacks: set[Callable[P, None]] = set()

        # Optional list of validator functions that will be called before triggering the event.
        self.validators = validators or []

    def subscribe(self, fn: Callable[P, None]) -> None:
        """
        Subscribe a callback function to the event. The function will be called when the event is triggered.
        Args:
            fn: The callback function to subscribe. It should accept the same parameters as the event.
        """
        self.callbacks.add(fn)

    def unsubscribe(self, fn: Callable[P, None]) -> None:
        """
        Unsubscribe a callback function from the event.
        Args:
            fn: The callback function to remove from callbacks.
        Raises:
            ValueError: If the callback function is not found in the list of subscribed callbacks.
        """
        if fn not in self.callbacks:
            raise ValueError('Callback not found')
        self.callbacks.discard(fn)

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

        for fn in self.callbacks:
            fn(*args, **kwargs)

    def clear(self) -> None:
        """Clear all subscribed callback functions from the event."""
        self.callbacks.clear()
