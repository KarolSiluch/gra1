import pygame
from map.tilemaps.tilemap import TileMap


class YSortCamera(TileMap):
    def render(self, display: pygame.Surface, camera_offset: pygame.Vector2):
        for tile in sorted(self.all_tiles_around(camera_offset, 35), key=lambda tile: (tile.z, tile.sprite.rect.bottom +
                                                                                       tile.sprite.sort_y_offset +
                                                                                       tile.sprite.render_offset.y)):
            if not tile.sprite.show:
                continue
            image, rect = tile.get_sprite()
            pos = rect.topleft - camera_offset + tile.sprite.render_offset
            display.blit(image, pos, special_flags=tile.special_flags)


class BackgroundCamera(TileMap):
    def update(self, dt, *args):
        for tile in self.tiles():
            tile.update(dt, *args)

    def render(self, display: pygame.Surface, camera_offset: pygame.Vector2):
        for tile in sorted(self.tiles(), key=lambda tile: (tile.z, tile.sprite.rect.bottom +
                                                           tile.sprite.sort_y_offset + tile.sprite.render_offset.y)):
            if not tile.sprite.show:
                continue
            depth = tile.z / 100
            image, rect = tile.get_sprite()
            pos = rect.topleft - camera_offset * depth + tile.sprite.render_offset
            pos[0] = pos[0] % (display.get_width() + image.get_width()) - image.get_width()
            display.blit(image, pos, special_flags=tile.special_flags)
