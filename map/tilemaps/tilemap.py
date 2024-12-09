from map.tiles.tile import Tile
import pygame


class TileMap:
    def __init__(self, tile_size=16) -> None:
        self._tile_size: int = tile_size
        self._tile_map: dict[tuple][list[Tile]] = {}
        self._offgrid_tiles = []

    @property
    def offgrid_tiles(self):
        return self._offgrid_tiles

    def add(self, tile: Tile, offgrid_tile):
        if offgrid_tile:
            self._offgrid_tiles.append(tile)
            return None

        x = tile.hitbox.centerx // self._tile_size
        y = tile.hitbox.centery // self._tile_size
        if (x, y) not in self._tile_map.keys():
            self._tile_map[(x, y)] = [tile]
        else:
            self._tile_map[(x, y)].append(tile)
        return (x, y)

    def tiles(self) -> list[Tile]:
        tiles = []
        for layer in self._tile_map.values():
            tiles.extend(layer)
        tiles.extend(self._offgrid_tiles)
        return tiles

    def grid_tiles_around_with_id(self, point: tuple[float], radius: int = 1):
        x_index = point[0] // self._tile_size
        y_index = point[1] // self._tile_size

        tiles = {}

        for y_offset in range(-radius, radius + 1):
            for x_offset in range(-radius, radius + 1):
                x, y = x_index + x_offset, y_index + y_offset
                if not (x, y) in self._tile_map.keys():
                    continue
                tiles[(x_offset, y_offset)] = self._tile_map[(x, y)]
        return tiles

    def grid_tiles_around(self, point: tuple[float], radius: int = 1) -> list[Tile]:
        x_index = point[0] // self._tile_size
        y_index = point[1] // self._tile_size

        tiles = []

        for y_offset in range(-radius, radius + 1):
            for x_offset in range(-radius, radius + 1):
                x, y = x_index + x_offset, y_index + y_offset
                if not (x, y) in self._tile_map.keys():
                    continue
                tiles.extend(self._tile_map[(x, y)])
        return tiles

    def all_tiles_around(self, point: tuple[float], radius: int = 1) -> list[Tile]:
        tiles = self.grid_tiles_around(point, radius)
        tiles.extend(self._offgrid_tiles)
        return tiles

    def update(self, dt, player_center, *args):
        for tile in self.all_tiles_around(player_center, 16):
            tile.update(dt, *args)

    def get_rect_collisions(self, rect: pygame.Rect, radius: int = 1):
        collisions: list[Tile] = []

        for tile in self.all_tiles_around(rect.center, radius):
            if rect is tile.hitbox:
                continue
            if not rect.colliderect(tile.hitbox):
                continue
            collisions.append(tile)

        return collisions

    def get_collisions(self, obj: Tile, radius: int = 1):
        return self.get_rect_collisions(obj.hitbox, radius)

    def remove_internal(self, sprite, place):
        if not place:
            if sprite not in self._offgrid_tiles:
                return
            self._offgrid_tiles.remove(sprite)
        else:
            if sprite not in self._tile_map[place]:
                return
            self._tile_map[place].remove(sprite)
            if len(self._tile_map[place]) == 0:
                del self._tile_map[place]
