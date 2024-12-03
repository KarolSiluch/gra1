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
        super().__init__(groups, 'player', image, self._state_machine.state, offgrid_tile=True, z=6, **pos)
        self.reset_collisions()
        self.hitbox.inflate_ip(-40, 0)

        self.direction = pygame.Vector2(0, 0)
        self._speed = 200

        self.jumps = 1

        self._charge = 0
        self._delta_charge = 100
        self._max_charge = 50

    @property
    def charge_fraction(self):
        return self._charge / self._max_charge

    @property
    def charge(self):
        return self._charge

    @property
    def speed(self):
        return self._speed

    @property
    def collisions(self):
        return self._collisions

    def reset_collisions(self):
        self._collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}

    def set_collision(self, *collisions):
        for collision in collisions:
            if collision not in self._collisions.keys():
                raise ValueError
            self._collisions[collision] = True

    def get_sprite(self):
        return (self._sprite.image(self._state_machine.direction()), self._sprite.rect)

    def self_charge(self, dt, direction: int):
        self._charge = sorted([0, self._charge + direction * dt * self._delta_charge, self._max_charge])[1]

    def update(self, dt, events):
        self.animate()
        self.reset_collisions()
        self.self_charge(dt, 2 * events['shift'] - 1)
        self._state_machine.update(dt, events)
        self._sprite.update(self.hitbox.center)
