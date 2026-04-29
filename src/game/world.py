from enum import Enum

from arcade import PymunkPhysicsEngine, SpriteList, color

from .area import Area
from .entities import Entity


class WorldTag(Enum):
    """Tags for categorizing entities in the world."""

    DEFAULT = 'default'
    STATIC = 'static'
    DYNAMIC = 'dynamic'


class World:
    def __init__(self):
        self.DEBUG_FLAG = True

        self.entities: dict[WorldTag, SpriteList] = {
            WorldTag.DEFAULT: SpriteList(),
            WorldTag.STATIC: SpriteList(),
            WorldTag.DYNAMIC: SpriteList(),
        }
        self.areas: list[Area] = []

        self._to_add = []
        self._to_remove = []
        self._to_add_areas = []
        self._to_remove_areas = []

        self.physics = PymunkPhysicsEngine()

    def add_entity(self, entity: Entity):
        self._to_add.append(entity)

    def remove_entity(self, entity: Entity):
        if not any(entity in group for group in self.entities.values()):
            return
        self._to_remove.append(entity)

    def add_area(self, area: Area):
        self._to_add_areas.append(area)

    def remove_area(self, area: Area):
        if area not in self.areas:
            return
        self._to_remove_areas.append(area)

    def update(self, dt: float):
        self._flush()

        for group in self.entities.values():
            group.update(dt)

        for area in self.areas:
            area.update(self.entities[WorldTag.DYNAMIC])

        self.physics.step(dt)

        self._flush()

    def draw(self):
        for group in self.entities.values():
            group.draw()

        if self.DEBUG_FLAG:
            for group in self.entities.values():
                for sprite in group:
                    sprite.draw_hit_box(color=color.RED, line_thickness=1)
                    sprite.draw_name()
            for area in self.areas:
                area.sprite.draw_hit_box(color=color.BLUE, line_thickness=1)

    def _flush(self):
        if self._to_add:
            for e in self._to_add:
                self._add_entity_immediately(e)
            self._to_add.clear()

        if self._to_remove:
            for e in self._to_remove:
                e.helpers.movement.physics = None
                for _, group in self.entities.items():
                    self.physics.remove_sprite(e)
                    if e in group:
                        group.remove(e)
            self._to_remove.clear()

        if self._to_add_areas:
            for a in self._to_add_areas:
                self.areas.append(a)
            self._to_add_areas.clear()

        if self._to_remove_areas:
            for a in self._to_remove_areas:
                if a in self.areas:
                    self.areas.remove(a)
            self._to_remove_areas.clear()

    def _add_entity_immediately(self, entity: Entity):
        entity.helpers.movement.physics = self.physics
        if entity.helpers.tags.has(WorldTag.STATIC.value):
            self.entities[WorldTag.STATIC].append(entity)
            self.physics.add_sprite(
                entity,
                body_type=PymunkPhysicsEngine.STATIC,
            )
        elif entity.helpers.tags.has(WorldTag.DYNAMIC.value):
            self.entities[WorldTag.DYNAMIC].append(entity)
            self.physics.add_sprite(
                entity,
                mass=1,
                friction=0.5,
                body_type=PymunkPhysicsEngine.DYNAMIC,
                moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            )
        else:
            self.entities[WorldTag.DEFAULT].append(entity)
