import pygame
from map.tiles.animated_tile import AnimatedTile
from player.states.state_machine import StateMachine


class Player(AnimatedTile):
    class Sprite(AnimatedTile.Sprite):
        def image(self, direction_x):
            if direction_x > 0:
                self.flip = False
            elif direction_x < 0:
                self.flip = True
            self.transform(flip=(self.flip, False))

            return self._final_image

    def __init__(self, groups, assets, **pos: tuple[int]) -> None:
        self._state_machine = StateMachine(self)
        image = assets['animations']
        super().__init__(groups, 'player', image, self._state_machine.state, offgrid_tile=True, **pos)
        self._direction = pygame.Vector2()
        self._velocity = 200

    @property
    def velocity(self):
        return self._velocity

    @property
    def direction(self):
        return self._direction

    def change_x_by(self, x):
        self.hitbox.x += x

    def change_y_by(self, y):
        self.hitbox.y += y

    def get_direction(self, events):
        self._direction.x = events['d'] - events['a']
        self._direction.y = events['s'] - events['w']

    def get_sprite(self):
        return (self._sprite.image(self._direction.x), self._sprite.rect)

    def update(self, dt, events):
        self.animate()
        self._state_machine.update(dt, events)
        self.get_direction(events)
