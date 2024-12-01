import pygame
from map.tilemaps.visible_sprites import YSortCamera
from map.tiles.tile import Tile


class Gameplay:
    def __init__(self):
        self.camera = YSortCamera()
        image = pygame.Surface((32, 32))
        image.fill('white')
        Tile([self.camera], 'test', image, center=(50, 50))

    def update(self, dt, events): ...

    def render(self, display: pygame.Surface):
        self.camera.render(display, pygame.Vector2(0, 0))
