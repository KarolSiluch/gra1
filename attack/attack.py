from map.tiles.tile import Tile
import pygame


class Attack(Tile):
    def __init__(self, groups, type, owner, hitbox: pygame.FRect, direction, power, **pos):
        super().__init__(groups, type, hitbox, offgrid_tile=True, **pos)
        self._owner = owner
        self._direction = direction
        self._power = power

    @property
    def owner(self):
        return self._owner

    @property
    def direction(self):
        return self._direction

    @property
    def power(self):
        return self._power

    def move_ip(self, pos, direction):
        self._direction = direction
        new_hitbox = self.sprite.image.get_rect(**pos)
        self.hitbox = new_hitbox
        self.sprite.update(self.hitbox.midbottom)

    def update(self, dt): ...
