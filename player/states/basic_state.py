from cooldown.cooldown import Cooldown


class BasicState:
    def __init__(self, context, possible_next_states: set[str], cooldown: int = 0) -> None:
        self._context = context
        self._cooldown = Cooldown(cooldown)
        self._possible_next_states = possible_next_states

    @property
    def possible_next_states(self):
        return self._possible_next_states

    @property
    def cooldown(self):
        return self._cooldown

    def _enter(self): ...

    def _exsit(self):
        self._cooldown.reset()

    def animate(self, dt):
        self._context.current_animation.update(dt)

    def update(self, dt, *args):
        self.animate(dt)

    def next_state(self, events): ...
