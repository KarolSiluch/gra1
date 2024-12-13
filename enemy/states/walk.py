from enemy.states.basic_state import BasicState
# import pygame
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from map.tilemaps.tilemap import TileMap
from math import copysign
from random import random


class EnemyWalkState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('walk')
        self._enemy_direction *= 0
        self._enemy_direction.x = copysign(1, self._context.prevoius_x_direction) * self._context.speed

    def get_direction(self):
        c_direction = copysign(1, self.enemy_direction.x)
        direction = self.enemy_direction.x
        map: TileMap = group_picker.get_group(GroupType.Collidable)
        souranding = map.grid_tiles_around_with_id(self._context.hitbox.center).keys()
        if (c_direction, -1) in souranding:
            direction *= -1
        elif (c_direction, 0) in souranding:
            direction *= -1
        elif (c_direction, 1) not in souranding:
            direction *= -1

        self.enemy_direction.x = direction

    def update(self, dt, player_center):
        self.get_direction()
        super().update(dt, player_center)

    def next_state(self, dt, player_center: tuple):
        if random() * 600 <= 340 * dt:
            return 'idle'
        # wx = player_center[0] - self.enemy_hitbox.centerx
        # wy = player_center[1] - self.enemy_hitbox.centery
        # if pygame.Vector2(wx, wy).magnitude() < 40:
