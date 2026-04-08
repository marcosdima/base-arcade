import arcade


class Entity(arcade.Sprite):
    '''Base class for all entities in the game.'''
    name: str
    life: int
    attack: int
    color: arcade.color


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


    def receive_damage(self, damage: int):
        self.life -= damage
        if self.life < 0:
            self.life = 0

    
    def is_alive(self) -> bool:
        return self.life > 0


    def draw_name(self, font_size: int = 12):
        arcade.draw_text(
            self.name,
            self.center_x,
            self.center_y,
            self.color,
            font_size,
            anchor_x="center",
            anchor_y="center",
        )
    
    