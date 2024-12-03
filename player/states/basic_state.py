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
        self._player_direction = pygame.Vector2(0, 0)
        self._gravity = gravity

    @property
    def possible_next_states(self):
        return self._possible_next_states

    @property
    def player_direction(self):
        return self._player_direction

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def player_hitbox(self) -> pygame.FRect:
        return self._context.hitbox

    def move(self, dt, direction: pygame.Vector2):
        tilemap: TileMap = group_picker.get_group(GroupType.Collidable)

        self._context.hitbox.x += direction.x * dt
        for tile in tilemap.get_collisions(self._context):
            if direction.x > 0:
                self._context.hitbox.right = tile.hitbox.left
                self._context.set_collision('right')
            elif direction.x < 0:
                self._context.hitbox.left = tile.hitbox.right
                self._context.set_collision('left')
            self._player_direction.x = 0

        self._context.hitbox.y += direction.y * dt
        for tile in tilemap.get_collisions(self._context):
            if direction.y > 0:
                self._context.hitbox.bottom = tile.hitbox.top
                self._context.set_collision('bottom')
            elif direction.y < 0:
                self._context.hitbox.top = tile.hitbox.top
                self._context.set_collision('top')
            self._player_direction.y = 0

    def _enter(self):
        self._player_direction = self._context.direction.copy()

    def _exsit(self):
        self._cooldown.reset()
        self._context.direction = self._player_direction.copy()

    def animate(self, dt):
        self._context.current_animation.update(dt)

    def update(self, dt, *args):
        self._player_direction.y = min(self._gravity * dt + self._player_direction.y, 600)
        self.move(dt, self.player_direction)
        self.animate(dt)

    def next_state(self, events): ...
