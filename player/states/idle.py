from player.states.basic_state import BasicState


class PlayerIdleState(BasicState):
    def _enter(self):
        super()._enter()
        self._context.change_animation('idle')
        self._context.jumps = 1

    def next_state(self, events):
        if events['d'] - events['a']:
            return 'run'
        if events['space']:
            if self._context.jumps:
                return 'jump'
