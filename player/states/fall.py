from player.states.basic_state import BasicState
from cooldown.cooldown import Cooldown


class PlayerFallState(BasicState):
    def __init__(self, context, possible_next_states, gravity=1500, cooldown=0):
        super().__init__(context, possible_next_states, gravity, cooldown)
        self.fall_jump_cooldown = Cooldown(30)

    def fall_jump(self):
        self.fall_jump_cooldown.timer()
        if self.fall_jump_cooldown():
            self._context.jumps = 0

    def _enter(self):
        super()._enter()
        self._context.change_animation('fall')
        self.fall_jump_cooldown.reset()

    def update(self, dt, events):
        self._gravity = 1050 if self._context.charge else 1500
        super().update(dt)
        self.fall_jump()

    def next_state(self, events):
        if self._context.collisions['bottom']:
            return 'run' if self._player_direction.x else 'idle'
        if events['space']:
            if self._context.jumps:
                return 'jump'
