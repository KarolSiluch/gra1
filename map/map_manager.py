import pygame
import json
from map.tilemaps.tilemap import TileMap
from map.tilemaps.visible_sprites import YSortCamera
from map.tiles.tile import Tile
from group_picker.settings import GroupType
from group_picker.group_picker import group_picker


class MapManager:
    def __init__(self, game, tile_size: int, map: str) -> None:
        self._game = game
        self._tile_size = tile_size
        self._camera_offset = pygame.Vector2()
        self._map = map
        self._sprite_groups = {
            GroupType.Visible: YSortCamera(tile_size),
            GroupType.Collidable: TileMap(tile_size),
        }
        self.enter()

        self._player_start_position = None

        try:
            self.load(f'{map}.json')
        except FileExistsError:
            pass

    @property
    def player_start_position(self):
        return self._player_start_position

    def enter(self):
        group_picker.init(self._sprite_groups)

    def load(self, path):
        f = open(path, 'r')
        map = json.load(f)
        f.close()
        for tile_data in map['tilemap']:
            self.create_tile(tile_data)

    def create_tile(self, tile_data):
        type = tile_data['type']
        variant = tile_data['variant']
        offgrid_tile = tile_data['offgrid_tile']
        layer = tile_data['z']
        pos: dict = tile_data['pos']

        if type in {'lab_tiles'}:
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Collidable)
            image = self._game.assets[type][variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type in {'border'}:
            groups = group_picker.get_groups(GroupType.Collidable)
            image = pygame.Surface((self._tile_size, self._tile_size))
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type == 'player':
            self._player_start_position = list(pos.values())[0]

        else:
            groups = group_picker.get_groups(GroupType.Visible)
            image = self._game.assets[type][variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

    def update(self, dt):
        self.get_camera_offset(dt)

    def get_camera_offset(self, dt):
        display = pygame.display.Info()
        offset_x = self._game.player.hitbox.centerx - display.current_w // 2 - self._camera_offset.x
        miltiplier = dt * 4
        self._camera_offset.x += offset_x * miltiplier
        offset_y = self._game.player.hitbox.centery - display.current_h // 2 - self._camera_offset.y
        self._camera_offset.y += offset_y * miltiplier

    def render(self, display: pygame.Surface):
        self._sprite_groups[GroupType.Visible].render(display, self._camera_offset)
