from entity.entity import Entity
from enemy.states.state_machine import StateMachine
from group_picker.group_picker import group_picker
from group_picker.settings import GroupType
from map.tilemaps.tilemap import TileMap


class Enemy(Entity):
    def __init__(self, groups, assets, **pos) -> None:
        super().__init__(groups, 'enemy', assets, StateMachine, **pos)
        self._speed = 40
        self.prevoius_x_direction = self._speed
        self._hp = 5

    def get_hit(self, power):
        self._hp -= power

    def get_hit_collisions(self):
        map: TileMap = group_picker.get_group(GroupType.Attacks)
        for attack in map.get_collisions(self):
            if attack.owner.tile_type == self.tile_type:
                continue
            self._state_machine.change_state('hit', attack)

    def update(self, dt, *args):
        self.get_hit_collisions()
        super().update(dt, *args)
        self.kill()

    def kill(self):
        if self._hp <= 0:
            super().kill()
