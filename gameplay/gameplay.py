import pygame
from map.tilemaps.visible_sprites import YSortCamera
from map.tiles.tile import Tile
from player.player import Player
from animation.animation import Animation
import support.support


class Gameplay:
    def __init__(self):
        self.import_assets()
        self.camera = YSortCamera()
        image = pygame.Surface((32, 32))
        image.fill('white')
        Tile([self.camera], 'test', image, center=(50, 50))
        self._player = Player([self.camera], self.assets['player'], center=(100, 100))

    def update(self, dt, events):
        self._player.update(dt, events)

    def render(self, display: pygame.Surface):
        self.camera.render(display, pygame.Vector2(self._player.hitbox.center) - (250, 150))

    def import_assets(self):
        player_path = 'assets/player/'
        self.assets = {
            'player': {
                'animations': {
                    'idle': Animation(support.support.import_cut_graphics((4, 1), f'{player_path}idle.png'), 7),
                    'run': Animation(support.support.import_cut_graphics((6, 1), f'{player_path}run.png'), 10),
                }
            }
        }
