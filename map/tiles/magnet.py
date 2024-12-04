from map.tiles.tile import Tile
import pygame

CONST = 80000


class Magnet(Tile):
    def __init__(self, groups, type, image, charge, sort_y_offset=0, offgrid_tile=False, z=5, special_flags=0, **pos):
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, special_flags, **pos)
        self.charge = charge

    def get_force(self, point: tuple[int], charge: int):
        vector = pygame.Vector2(point[0] - self.hitbox.centerx, point[1] - self.hitbox.centery)
        if not vector:
            return pygame.Vector2(0, 0)
        distance = vector.magnitude()
        force = CONST * self.charge * charge / distance ** 2

        vector.scale_to_length(force)
        return vector
