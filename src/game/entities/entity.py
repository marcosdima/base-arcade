import arcade
from enum import Enum
from .helpers import Helpers


class EntityGroup(Enum):
    STATIC = 0
    DYNAMIC = 1


class Entity(arcade.Sprite):
    '''Base class for all entities in the game.'''
    def __init__(
        self,
        name: str = "Entity",
        size: tuple[int] = (32, 32),
    ):
        super().__init__()
        
        self.name = name
        self.size = size
        self._name_text = None
        self._name_text_font_size = -1

        # Hide the default sprite texture; entity debug rendering uses hitbox + label only.
        texture_size = max(self.size)
        self.texture = arcade.make_soft_square_texture(
            texture_size,
            arcade.color.WHITE,
            center_alpha=0,
            outer_alpha=0,
        )

        # Updates hitbox to match the specified size.
        width, height = self.size
        half_width = width / 2
        half_height = height / 2
        self.hit_box = arcade.hitbox.HitBox(
            [
                (-half_width, -half_height),
                (half_width, -half_height),
                (half_width, half_height),
                (-half_width, half_height),
            ]
        )

        # Set helpers.
        self.helpers = Helpers(self)


    def draw_name(self, font_size: int = 12):
        if self._name_text is None or self._name_text_font_size != font_size:
            self._name_text = arcade.Text(
                text=self.name,
                x=self.center_x,
                y=self.center_y,
                color=arcade.color.WHITE,
                font_size=font_size,
                anchor_x="center",
                anchor_y="center",
            )
            self._name_text_font_size = font_size

        self._name_text.text = self.name
        self._name_text.x = self.center_x
        self._name_text.y = self.center_y
        self._name_text.color = arcade.color.WHITE
        self._name_text.rotation = self.angle
        self._name_text.draw()
    
    