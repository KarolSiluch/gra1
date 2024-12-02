from player.states.basic_state import BasicState


class PlayerIdleState(BasicState):
    def _enter(self):
        self._context.change_animation('idle')

    def next_state(self, events):
        if self._context.direction.magnitude():
            return 'run'
