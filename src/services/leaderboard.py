from datetime import datetime
import json

from ..engine import Functions
from ..engine.core.event import Event


class Leaderboard:
    _instance: 'Leaderboard' = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return

        self.leaderboard_file_path = Functions.resource_path('assets/leaderboard.json')
        self._initialized = True
        self.load()
        self.score_added = Event[[str, int]]()

    @classmethod
    def add_score(cls, player_name: str, score: int):
        """Agrega un nuevo puntaje al leaderboard."""
        entry = {
            'name': player_name,
            'score': score,
            'date': datetime.now().isoformat(),
        }

        cls._instance.leaderboard.append(entry)
        cls._instance.leaderboard.sort(key=lambda x: x['score'], reverse=True)
        cls._instance.save()
        cls._instance.score_added.trigger(player_name, score)

    @classmethod
    def get_top_scores(cls, limit: int = 10) -> list[dict]:
        """Obtiene los mejores puntajes, limitado a la cantidad especificada."""
        return cls._instance.leaderboard[:limit]

    @classmethod
    def get_all_scores(cls) -> list[dict]:
        """Obtiene todos los puntajes."""
        return cls._instance.leaderboard

    @classmethod
    def clear(cls):
        """Limpia el leaderboard."""
        cls._instance.leaderboard = []
        cls._instance.save()

    @classmethod
    def save(cls):
        """Guarda el leaderboard en el archivo JSON."""
        with open(cls._instance.leaderboard_file_path, 'w') as f:
            json.dump(cls._instance.leaderboard, f, indent=4)

    @classmethod
    def load(cls):
        """Carga el leaderboard desde el archivo JSON."""
        try:
            with open(cls._instance.leaderboard_file_path) as f:
                data = json.load(f)
                cls._instance.leaderboard = data if isinstance(data, list) else []
                # Asegurar que esté ordenado por score descendente
                cls._instance.leaderboard.sort(
                    key=lambda x: x.get('score', 0), reverse=True
                )
        except (FileNotFoundError, json.JSONDecodeError):
            cls._instance.leaderboard = []
