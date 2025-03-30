from map.tiles.tile import Tile


class Slope(Tile):
    def __init__(self, groups, type, image, sort_y_offset=0, offgrid_tile=False, z=5, special_flags=0, **pos):
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, special_flags, **pos)
        self._offset = lambda x: x + 5

    def get_horizontal_collision(self, rect, collisions: set):
        return False

    def get_vertical_collision(self, rect, collisions: set):
        if not self.hitbox.left - 4 < rect.centerx < self.hitbox.right:
            return False
        top = self.hitbox.bottom - min(self._offset(rect.centerx - self.hitbox.left), 16)
        if rect.bottom < top:
            return False
        return True

    def vertical_collision(self, entity, direction):
        if direction.y > 0:
            entity.hitbox.bottom = self.hitbox.bottom - min(self._offset(entity.hitbox.centerx - self.hitbox.left), 16)
            entity.set_collision('bottom')
        elif direction.y < 0:
            entity.hitbox.top = self.hitbox.bottom
            entity.set_collision('top')
