type Validator = callable[[object], bool]

class Event:
    def __init__(self):
        self.callbacks: list[callable] = []
        self.validators: list[Validator] = []

    
    def suscribe(self, fn: callable):
        self.callbacks.append(fn)


    def unsuscribe(self, fn: callable):
        if fn in self.callbacks:
            self.callbacks.remove(fn)


    def trigger(self, *args, **kwargs):
        for fn in self.callbacks:
            if all(validator(arg) for validator, arg in zip(self.validators, args)):
                fn(*args, **kwargs)


    def clear(self):
        self.callbacks.clear()
