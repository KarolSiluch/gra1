from player.states.basic_state import BasicState
# import pygame


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
        if self._player_direction.y >= 0:
            return 'fall'
