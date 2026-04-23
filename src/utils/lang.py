import enum
import json
from .functions import Functions
from .path import resource_path

class Language(enum.Enum):
    ENGLISH = "en"
    SPANISH = "es"


class Lang:
    _instance = None

    
    def __new__(cls, default_language: (Language | str) = Language.ENGLISH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, default_language: (Language | str) = Language.ENGLISH):
        if getattr(self, "_initialized", False):
            return
        
        self._initialized = True
        self.translations_path = resource_path("assets/lang")
        self.current_language = default_language if isinstance(default_language, Language) else Language(default_language)
        self.load_translations()


    def load_translations(self):
        self.translations: dict[Language, dict] = {}
        for lang in Language:
            name = lang.value
            try:
                with open(f"{self.translations_path}/{name}.json", "r", encoding="utf-8") as f:
                    translation = json.load(f)
                    self.translations[lang] = translation
            except FileNotFoundError:
                print(f"Translation file for {name} not found.")


    def check_structure(self) -> dict[Language, list[str]]:
        report: dict[Language, list[str]] = {}
        
        translation_keys = {
            lang: Functions.get_dict_keys(translation)
            for lang, translation in self.translations.items()
        }

        all_keys = set().union(*translation_keys.values())

        for lang, keys in translation_keys.items():
            missing = all_keys - set(keys)
            report[lang] = list(missing)

        return report
    

    def get_current_translation(self) -> dict:
        return self.translations.get(self.current_language, {})


    @classmethod
    def get(cls, key: str) -> str:
        parsed_key = key.split(".")

        data = cls._instance.get_current_translation()

        for part in parsed_key:
            data = data.get(part, None)
            if data is None:
                raise AttributeError(f"Key '{key}' not found in Lang ({cls._instance.current_language.value}).")
            
        return data




        