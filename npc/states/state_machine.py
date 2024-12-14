from enemy.states.basic_state import BasicState
from enemy.states.idle import EnemyIdleState


class StateMachine:
    def __init__(self, context) -> None:
        self._state = 'idle'
        self._states = {
            'idle': EnemyIdleState(context, {}),
        }
        self._current_state: BasicState = self._states[self._state]

    @property
    def state(self):
        return self._state

    def change_state(self, state: str, *args):
        if not state:
            return
        if state not in self._current_state.possible_next_states:
            return
        if not self._states[state].cooldown():
            return
        self._current_state._exsit()
        self._current_state = self._states[state]
        self._current_state._enter(*args)
        self._state = state

    def direction(self):
        return self._current_state.enemy_direction.x

    def update(self, dt, player_center):
        self._current_state.update(dt, player_center)
        for state in self._states.values():
            state.cooldown.timer()
        self.change_state(self._current_state.next_state(dt, player_center))
