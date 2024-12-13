from player.states.run import PlayerRunState
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from attack.attack import Attack
from math import copysign
import pygame


class PlayerAttackState(PlayerRunState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('attack')
        self._context.jumps = 1
        self._attack = self.create_attack()

    def _exsit(self):
        super()._exsit()
        self._attack.kill()

    def get_attack_pos(self):
        direction_x = copysign(1, self._context.prevoius_x_direction)
        pos = {'centery': self.player_hitbox.centery}
        if direction_x > 0:
            pos['left'] = self.player_hitbox.right - 3
        else:
            pos['right'] = self.player_hitbox.left + 3
        return pos

    def update(self, dt, events):
        super().update(dt, events)
        direction_x = copysign(1, self._context.prevoius_x_direction)
        self._attack.move_ip(self.get_attack_pos(), direction_x)

    def create_attack(self):
        groups = group_picker.get_groups(GroupType.Attacks)
        direction_x = copysign(1, self._context.prevoius_x_direction)
        attack_hitbox = pygame.Surface((18, 20))
        pos = self.get_attack_pos()
        return Attack(groups, 'attack', self._context, attack_hitbox, direction_x, 1, **pos)

    def next_state(self, events):
        if events['space']:
            if self._context.jumps:
                return 'jump'
        if self._context.current_animation.done:
            if self._player_direction.magnitude():
                return 'run'
            if self._player_direction.magnitude() == 0:
                return 'idle'
            if not self._context.collisions['bottom']:
                return 'fall'
