from player.states.basic_state import BasicState
# import pygame
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from map.tilemaps.tilemap import TileMap
from math import copysign


class PlayerJumpState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('jump')
        self._player_direction.y = -340
        self._context.jumps -= 1

    def _exsit(self):
        self._player_direction.y = 0
        super()._exsit()

    def next_state(self, events):
        if self._player_direction.y < 0:
            return

        if self._context.charge_fraction >= 0.5:
            if not self.player_direction.x:
                tilemap: TileMap = group_picker.get_group(GroupType.Collidable)
                souranding = tilemap.grid_tiles_around_with_id(self._context.hitbox.center).keys()
                x = copysign(1, self._context.prevoius_x_direction)
                if (x, 0) in souranding and (x, 1) in souranding:
                    if tilemap.get_rect_collisions(self._context.slide_hitbox):
                        return 'slide'

        return 'fall'
