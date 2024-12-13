from enemy.states.basic_state import BasicState
from attack.attack import Attack
from math import copysign


class EnemyHitState(BasicState):
    def _enter(self, attack: Attack):
        super()._enter()
        self._context.change_animation('idle')
        self._enemy_direction.x = attack._direction * 300
        self._context.get_hit(attack.power)

    def accelerate(self, dt):
        acceleration = copysign(1, -self.enemy_direction.x) * 1000
        self._enemy_direction.x += acceleration * dt
        print(self._enemy_direction.x)

    def update(self, dt, player_center):
        self.accelerate(dt)
        super().update(dt, player_center)

    def next_state(self, dt, player_center: tuple):
        if abs(self._enemy_direction.x) < 10:
            return 'idle'
