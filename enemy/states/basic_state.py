from cooldown.cooldown import Cooldown
import pygame
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from map.tilemaps.tilemap import TileMap


class BasicState:
    def __init__(self, context, possible_next_states: set[str], gravity: int = 1500, cooldown: int = 0) -> None:
        self._context = context
        self._cooldown = Cooldown(cooldown)
        self._possible_next_states = possible_next_states
        self._enemy_direction = pygame.Vector2(0, 0)
        self._gravity = gravity

    @property
    def possible_next_states(self):
        return self._possible_next_states

    @property
    def enemy_direction(self):
        return self._enemy_direction

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def enemy_hitbox(self) -> pygame.FRect:
        return self._context.hitbox

    def move(self, dt, direction: pygame.Vector2):
        tilemap: TileMap = group_picker.get_group(GroupType.Collidable)

        self._context.hitbox.y += direction.y * dt
        for tile in tilemap.get_vertical_collisions(self._context.hitbox, 2):
            tile.vertical_collision(self._context, direction)
            self._enemy_direction.y = 0

        self._context.hitbox.x += direction.x * dt
        for tile in tilemap.get_horizontal_collisions(self._context.hitbox, 2):
            tile.horizontal_collision(self._context, direction)
            self._enemy_direction.x = 0

    def _enter(self, *args):
        self._enemy_direction = self._context.direction.copy()

    def _exsit(self):
        self._cooldown.reset()
        self._context.direction = self._enemy_direction.copy()

    def animate(self, dt):
        self._context.current_animation.update(dt)

    def update(self, dt, player_center):
        self.move(dt, self.enemy_direction)
        self.animate(dt)
        self.enemy_direction.y = min(self._gravity * dt + self.enemy_direction.y, 600)
        if direction := self.enemy_direction.x:
            self._context.prevoius_x_direction = direction

    def next_state(self, dt, player_center): ...
