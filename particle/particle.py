from map.tiles.tile import Tile
from animation.animation import Animation
from math import sin
import pygame


class Particle(Tile):
    def __init__(self, groups, type, animation, velocity: pygame.Vector2, acceleration: pygame.Vector2, sort_y_offset=0,
                 offgrid_tile=False, z=5, special_flags=0, **pos):
        self._animation: Animation = animation.copy()
        super().__init__(groups, type, self.animation.img(), sort_y_offset, offgrid_tile, z, special_flags, **pos)
        self._velocity = velocity
        self._acceleration = acceleration

    @property
    def animation(self):
        return self._animation

    def animate(self):
        self.sprite.new_image(self._animation.img())

    def move(self, dt):
        self.hitbox.x += sin(self._animation.frame * dt) * 100 * dt
        self._velocity.x = sorted([-200, self._velocity.x + self._acceleration.x, 200])[1]
        self._velocity.y = sorted([-200, self._velocity.y + self._acceleration.y, 200])[1]
        self.hitbox.x += self._velocity.x * dt
        self.hitbox.y += self._velocity.y * dt
        self.sprite.update(self.hitbox.center)

    def update(self, dt):
        self._animation.update(dt)
        self.animate()
        self.move(dt)
        if self.animation.done:
            self.kill()
