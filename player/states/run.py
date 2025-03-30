from player.states.basic_state import BasicState


class PlayerRunState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('run')
        self._player_direction *= 0
        self._context.jumps = 1
        self._air_time = 0

    def get_direction(self, events):
        self._player_direction.x = (events['d'] - events['a']) * self._context.speed

    def update(self, dt, events):
        super().update(dt)
        self.get_direction(events)
        if self._context.collisions['bottom']:
            self._air_time = 0
        self._air_time += dt

    def next_state(self, events):
        if self._player_direction.magnitude() == 0:
            return 'idle'
        if not self._context.collisions['bottom']:
            if self._air_time > 0.03:
                return 'fall'
        if events['space']:
            if self._context.jumps:
                return 'jump'
        if events['mouse1']:
            return 'attack'
