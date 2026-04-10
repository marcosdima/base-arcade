import arcade


class Entity(arcade.Sprite):
    '''Base class for all entities in the game.'''
    name: str
    life: int
    attack: int
    color: arcade.color
    _name_text: arcade.Text | None
    _name_text_font_size: int


    def __init__(
        self,
        name: str = "Entity",
        life: int = 3,
        attack: int = 1,
        size: tuple[int] = (32, 32),
        color: arcade.color = arcade.color.WHITE,
    ):
        super().__init__()
        
        self.name = name
        self.life = life
        self.attack = attack
        self.color = color
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


    def receive_damage(self, damage: int):
        self.life -= damage
        if self.life < 0:
            self.life = 0

    
    def is_alive(self) -> bool:
        return self.life > 0


    def draw_name(self, font_size: int = 12):
        if self._name_text is None or self._name_text_font_size != font_size:
            self._name_text = arcade.Text(
                self.name,
                self.center_x,
                self.center_y,
                self.color,
                font_size,
                anchor_x="center",
                anchor_y="center",
            )
            self._name_text_font_size = font_size

        self._name_text.text = self.name
        self._name_text.x = self.center_x
        self._name_text.y = self.center_y
        self._name_text.color = self.color
        self._name_text.rotation = self.angle
        self._name_text.draw()
    
    