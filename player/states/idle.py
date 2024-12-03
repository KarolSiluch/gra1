from player.states.basic_state import BasicState
import pygame


class PlayerIdleState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('idle')
        self._context.jumps = 1

    def external_force(self):
        force = super().external_force()
        return pygame.Vector2(force.x // 100, force.y)

    def next_state(self, events):
        if events['d'] - events['a']:
            return 'run'
        if not self._context.collisions['bottom']:
            return 'fall'
        if events['space']:
            if self._context.jumps:
                return 'jump'
