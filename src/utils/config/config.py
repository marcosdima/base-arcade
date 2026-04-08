import json
import enum


class ConfigKey(enum.Enum):
    WINDOW_WIDTH = 'window-width'
    WINDOW_HEIGHT = 'window-height'
    BACKGROUND_COLOR = 'window-background_color'
    TITLE = 'title'

    # Input.
    MOVE_UP = 'input-movement-up'
    MOVE_DOWN = 'input-movement-down'
    MOVE_LEFT = 'input-movement-left'
    MOVE_RIGHT = 'input-movement-right'


class Config:
    config_file_path: str = 'src/utils/config/config.json'
    _instance: 'Config' = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.load()


    @classmethod
    def get(cls, key: ConfigKey, default=None):
        parsed_key = key.value.split('-')
        current = cls._instance.config
        
        for part in parsed_key:
            if part in current:
                current = current[part]
            else:
                return default
        
        return current
    

    @classmethod
    def set(cls, key: ConfigKey, value):
        cls._instance.config[key.value] = value


    @classmethod
    def save(cls):
        with open(cls._instance.config_file_path, 'w') as f:
            json.dump(cls._instance.config, f, indent=4)


    @classmethod
    def load(cls):
        with open(cls._instance.config_file_path, 'r') as f:
            cls._instance.config = json.load(f)