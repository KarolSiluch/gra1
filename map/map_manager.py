import pygame
import json
from map.tilemaps.tilemap import TileMap
from map.tilemaps.visible_sprites import YSortCamera, BackgroundCamera
from map.tiles.tile import Tile
from map.tiles.background_tile import BackgroundTile
from group_picker.settings import GroupType
from group_picker.group_picker import group_picker
from map.tiles.magnet import Magnet
from random import randint, choice, random
from enemy.enemy import Enemy
from entity.entity import Entity
from npc.states.state_machine import StateMachine as KakineAI
from map.tiles.slope import Slope


class MapManager:
    def __init__(self, game, tile_size: int, map: str) -> None:
        self._game = game
        self._tile_size = tile_size
        self._camera_offset = pygame.Vector2()
        self._map = map
        self._sprite_groups = {
            GroupType.Visible: YSortCamera(tile_size),
            GroupType.Collidable: TileMap(tile_size),
            GroupType.Magnets: TileMap(tile_size),
            GroupType.Background: BackgroundCamera(tile_size),
            GroupType.Particles: TileMap(tile_size),
            GroupType.Enemies: TileMap(tile_size),
            GroupType.Attacks: TileMap(tile_size),
        }
        self.enter()
        self.create_a_background()

        self._player_start_position = None

        try:
            self.load(f'{map}.json')
        except FileExistsError:
            pass

    @property
    def player_start_position(self):
        return self._player_start_position

    def create_a_background(self):
        screen_h = pygame.display.Info().current_h
        group = group_picker.get_group(GroupType.Background)
        for _ in range(10):
            assets = self._game.assets['background_buildings']
            image = choice(assets)
            z = randint(20, 70)
            x = random() * 99999
            pos = (x, screen_h - randint(-10, 10))
            BackgroundTile([group], 'background_buildings', image, offgrid_tile=True, z=z, midbottom=pos)
        for _ in range(8):
            assets = self._game.assets['clouds']
            image: pygame.Surface = choice(assets)
            z = randint(10, 60)
            y = randint(-50, int(screen_h * 0.3))
            x = random() * 99999
            wind = randint(3, 15)
            BackgroundTile([group], 'background_buildings', image, wind, offgrid_tile=True, z=z, topleft=(x, y))

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

        if type in {'lab_tiles', 'container1', 'container2', 'gravel'}:
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Collidable)
            image = self._game.assets[type][variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type in {'border'}:
            groups = group_picker.get_groups(GroupType.Collidable)
            image = pygame.Surface((self._tile_size, self._tile_size))
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif 'magnet' in type:
            charge = variant + 1 if '+' in type else -variant - 1
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Collidable, GroupType.Magnets)
            image = self._game.assets[type][variant]
            Magnet(groups, type, image, charge=charge, offgrid_tile=offgrid_tile, z=layer, **pos)

        elif type in {'enemy'}:
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Enemies)
            Enemy(groups, self._game.assets['enemy'], **pos)

        elif type in {'kakine'}:
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Enemies)
            Entity(groups, 'kakine', self._game.assets['kakine'], KakineAI, **pos)

        elif type in {'slope'}:
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Collidable)
            Slope(groups, 'slope', self._game.assets['slope'][0], **pos)

        elif type == 'player':
            self._player_start_position = list(pos.values())[0]
            groups = group_picker.get_groups(GroupType.Visible, GroupType.Enemies)

        else:
            groups = group_picker.get_groups(GroupType.Visible)
            image = self._game.assets[type][variant]
            Tile(groups, type, image, offgrid_tile=offgrid_tile, z=layer, **pos)

    def update(self, dt):
        p_center = self._game.player.hitbox.center
        self._sprite_groups[GroupType.Background].update(dt)
        self._sprite_groups[GroupType.Particles].update(dt, p_center)
        self._sprite_groups[GroupType.Enemies].update(dt, p_center, p_center)
        self._sprite_groups[GroupType.Attacks].update(dt, p_center)
        self.get_camera_offset(dt)

    def get_camera_offset(self, dt):
        display = pygame.display.Info()
        offset_x = self._game.player.hitbox.centerx - display.current_w // 2 - self._camera_offset.x
        miltiplier = dt * 4
        self._camera_offset.x += offset_x * miltiplier
        offset_y = self._game.player.hitbox.centery - display.current_h // 2 - self._camera_offset.y - 40
        self._camera_offset.y += offset_y * miltiplier

    def render(self, display: pygame.Surface):
        self._sprite_groups[GroupType.Background].render(display, self._camera_offset)
        self._sprite_groups[GroupType.Visible].render(display, self._camera_offset)
