import pygame
from map.tiles.animated_tile import AnimatedTile
from player.states.state_machine import StateMachine


class Entity(AnimatedTile):
    class Sprite(AnimatedTile.Sprite):
        def image(self, direction_x):
            if direction_x > 0:
                self.flip = False
            elif direction_x < 0:
                self.flip = True
            self.transform(flip=(self.flip, False))

            return self._final_image

    def __init__(self, groups, type, assets, state_machine, **pos: tuple[int]) -> None:
        self._state_machine: StateMachine = state_machine(self)
        image = assets['animations']
        super().__init__(groups, type, image, self._state_machine.state, offgrid_tile=True, z=6, **pos)
        self.reset_collisions()
        self.hitbox.inflate_ip(-40, 0)
        self.slide_hitbox = self.hitbox.copy().inflate(2, 0)

        self.direction = pygame.Vector2(0, 0)
        self._speed = 200
        self.prevoius_x_direction = self._speed

    @property
    def speed(self):
        return self._speed

    @property
    def collisions(self):
        return self._collisions

    def set_state_machine(self, machine):
        self._state_machine = machine

    def reset_collisions(self):
        self._collisions = {'top': False, 'bottom': False, 'right': False, 'left': False}

    def set_collision(self, *collisions):
        for collision in collisions:
            if collision not in self._collisions.keys():
                raise ValueError
            self._collisions[collision] = True

    def get_sprite(self):
        return (self._sprite.image(self._state_machine.direction()), self._sprite.rect)

    def update(self, dt, *args):
        self.animate()
        self.reset_collisions()
        self._state_machine.update(dt, *args)
        self.slide_hitbox.center = self.hitbox.center
        self._sprite.update(self.hitbox.midbottom)
