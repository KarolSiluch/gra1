from player.states.basic_state import BasicState
import pygame
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from map.tilemaps.tilemap import TileMap
from math import copysign


class PlayerSlideState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('slide')
        self._context.jumps = 1
        self.player_direction.y = 0

    def apply_force(self, dt):
        force = self.total_force()
        self.player_direction.x = min(force.x * dt + self.player_direction.x, 600)
        self.player_direction.y = min(force.y * dt + self.player_direction.y, 70)

    def external_force(self):
        force = super().external_force()
        return pygame.Vector2(0, force.y)

    def next_state(self, events):
        if events['space']:
            self.player_direction.x = -self._context.prevoius_x_direction
            return 'jump'

        if self._context.collisions['bottom']:
            return 'idle'

        if self._context.charge_fraction < 0.5:
            return 'fall'

        if self.player_direction.y < 0:
            return 'fall'

        tilemap: TileMap = group_picker.get_group(GroupType.Collidable)
        souranding = tilemap.grid_tiles_around_with_id(self._context.hitbox.center).keys()
        x = copysign(1, self._context.prevoius_x_direction)
        if (x, 1) in souranding:
            return
        if tilemap.get_rect_collisions(self._context.slide_hitbox):
            return 'fall'
