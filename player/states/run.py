from player.states.basic_state import BasicState
import pygame


class PlayerRunState(BasicState):
    def _enter(self):
        self._context.change_animation('run')

    def move(self, dt, direction: pygame.Vector2):
        self._context.change_x_by(direction.x * self._context.velocity * dt)
        self._context.change_y_by(direction.y * self._context.velocity * dt)
        self._context.sprite.update(self._context.hitbox.center)

    def update(self, dt):
        super().update(dt)
        self.move(dt, self._context.direction)

    def next_state(self, events):
        if not self._context.direction.magnitude():
            return 'idle'
