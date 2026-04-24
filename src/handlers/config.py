import json
import enum
from ..utils.event import Event
from ..utils.path import resource_path


class ConfigKey(enum.Enum):
    # Game variables.
    TITLE = 'title'

    # Settings.
    LANGUAGE = 'language'
    WINDOW_WIDTH = 'window-width'
    WINDOW_HEIGHT = 'window-height'
    BACKGROUND_COLOR = 'window-background_color'
    
    # Input.
    MOVE_UP = 'input-movement-up'
    MOVE_DOWN = 'input-movement-down'
    MOVE_LEFT = 'input-movement-left'
    MOVE_RIGHT = 'input-movement-right'


class Config:
    _instance: 'Config' = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        self.config_file_path = resource_path("assets/config.json")
        self._initialized = True
        self.load()
        self.field_changed = Event[[ConfigKey, any]]()


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
        cls._instance.field_changed.trigger(key, value)


    @classmethod
    def save(cls):
        with open(cls._instance.config_file_path, 'w') as f:
            json.dump(cls._instance.config, f, indent=4)


    @classmethod
    def load(cls):
        with open(cls._instance.config_file_path, 'r') as f:
            cls._instance.config = json.load(f)