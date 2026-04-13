import enum
import json

from ..functions import Functions

class Language(enum.Enum):
    ENGLISH = "en"
    SPANISH = "es"


class Lang:
    _instance = None

    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, lang: Language = Language.ENGLISH):
        if getattr(self, "_initialized", False):
            return
        
        self._initialized = True
        self.current_language = lang
        self.load_translations()


    def load_translations(self):
        self.translations: dict[Language, dict] = {}
        for lang in Language:
            name = lang.value
            try:
                with open(f"src/utils/lang/files/{name}.json", "r", encoding="utf-8") as f:
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




        