from player.states.basic_state import BasicState
from player.states.run import PlayerRunState
from player.states.idle import PlayerIdleState


class StateMachine:
    def __init__(self, context) -> None:
        self._state = 'idle'
        self._states = {
            'idle': PlayerIdleState(context, {'run'}),
            'run': PlayerRunState(context, {'idle'}),
        }
        self._current_state: BasicState = self._states[self._state]

    @property
    def state(self):
        return self._state

    def change_state(self, state: str):
        if not state:
            return
        if state not in self._current_state.possible_next_states:
            return
        if not self._states[state].cooldown():
            return
        self._current_state._exsit()
        self._current_state = self._states[state]
        self._current_state._enter()
        self._state = state

    def update(self, dt, events, *args):
        self._current_state.update(dt, *args)
        for state in self._states.values():
            state.cooldown.timer()
        self.change_state(self._current_state.next_state(events))
        # if state := self.current_state.next_state(): self.change_state(state)]
