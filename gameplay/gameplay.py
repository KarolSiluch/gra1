import pygame
from map.map_manager import MapManager
from player.player import Player
from animation.animation import Animation
import support.support
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from support.support import import_cut_graphics
from gi.gi import GI


class Gameplay:
    def __init__(self):
        self.import_assets()
        self._map_manager = MapManager(self, 16, 'map1')
        groups = group_picker.get_groups(GroupType.Visible)
        self.player = Player(groups, self._assets['player'], center=self._map_manager.player_start_position)
        self.gi = GI(self.player)

    @property
    def assets(self):
        return self._assets

    def update(self, dt, events):
        self._map_manager.update(dt)
        self.player.update(dt, events)

    def render(self, display: pygame.Surface):
        self._map_manager.render(display)
        self.gi.render(display)

    def import_assets(self):
        player_path = 'assets/player/'
        self._assets = {
            'player': {
                'animations': {
                    'idle': Animation(support.support.import_cut_graphics((4, 1), f'{player_path}idle.png'), 7),
                    'run': Animation(support.support.import_cut_graphics((6, 1), f'{player_path}run.png'), 10),
                    'fall': Animation(support.support.import_cut_graphics((1, 1), f'{player_path}fall.png')),
                    'jump': Animation(support.support.import_cut_graphics((1, 1), f'{player_path}jump.png')),
                }
            },
            'lab_tiles': import_cut_graphics((3, 3), 'assets/tiles/lab_tiles.png'),
            'magnet+': import_cut_graphics((5, 1), 'assets/tiles/magnet+.png'),
            'magnet-': import_cut_graphics((5, 1), 'assets/tiles/magnet-.png'),
            'background_buildings': import_cut_graphics((6, 1), 'assets/background_buildings.png'),
            'clouds': import_cut_graphics((2, 1), 'assets/clouds.png'),
            'container1': import_cut_graphics((5, 3), 'assets/tiles/container1.png'),
            'container2': import_cut_graphics((5, 3), 'assets/tiles/container2.png')
        }
