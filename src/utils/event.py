from typing import Callable, Generic, ParamSpec

P = ParamSpec("P")
Validator = Callable[..., bool]


class Event(Generic[P]):
    def __init__(self, validators: list[Validator] | None = None):
        self.callbacks: set[Callable[P, None]] = set()
        self.validators = validators or []


    def subscribe(self, fn: Callable[P, None]) -> None:
        self.callbacks.add(fn)


    def unsubscribe(self, fn: Callable[P, None]) -> None:
        if not fn in self.callbacks:
            raise ValueError("Callback not found")
        self.callbacks.discard(fn)


    def trigger(self, *args: P.args, **kwargs: P.kwargs) -> None:
        if not all(v(*args, **kwargs) for v in self.validators):
            raise ValueError("Event validation failed")

        for fn in self.callbacks:
            fn(*args, **kwargs)


    def clear(self) -> None:
        self.callbacks.clear()