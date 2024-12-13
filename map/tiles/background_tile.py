from map.tiles.tile import Tile


class BackgroundTile(Tile):
    def __init__(self, groups, type, image, direction_x=0,
                 sort_y_offset=0, offgrid_tile=False, z=5, special_flags=0, **pos):
        super().__init__(groups, type, image, sort_y_offset, offgrid_tile, z, special_flags, **pos)
        self._direction_x = direction_x

    def update(self, dt):
        self.hitbox.x += self._direction_x * dt * self._z / 100
        self._sprite.update(self.hitbox.midbottom)
