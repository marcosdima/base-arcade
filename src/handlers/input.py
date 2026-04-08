import arcade


class InputHandler:
    def __init__(self):
        self.keys: dict[int, bool] = {}
        self.mouse_position: tuple[int, int] = (0, 0)
        self.mouse_d: tuple[int, int] = (0, 0)


    def update_mouse(self, x: int, y: int, dx: int, dy: int):
        self.mouse_position = (x, y)
        self.mouse_d = (dx, dy)


    def key_pressed(self, key: int):
        self.keys[key] = True


    def key_released(self, key: int):
        self.keys[key] = False


    def is_pressed(self, key: int | str) -> bool:
        resolved_key = key if isinstance(key, int) else getattr(arcade.key, key.upper(), None)
        return self.keys.get(resolved_key, False)


    # Backward-compatible alias while old callsites are migrated.
    def is_presed(self, key: int | str) -> bool:
        return self.is_pressed(key)
    