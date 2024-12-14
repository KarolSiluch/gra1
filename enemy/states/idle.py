from enemy.states.basic_state import BasicState
# import pygame
from random import random


class EnemyIdleState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('idle')
        self._enemy_direction.x = 0

    def next_state(self, dt, player_center: tuple):
        # wx = player_center[0] - self.enemy_hitbox.centerx
        # wy = player_center[1] - self.enemy_hitbox.centery
        # if pygame.Vector2(wx, wy).magnitude() > 40:
        #     return 'walk'
        if not self._context.collisions['bottom']:
            return
        if random() * 600 <= 340 * dt:
            return 'walk'
