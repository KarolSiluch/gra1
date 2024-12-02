from group_picker.settings import GroupType, InvalidGroupTypeError
from map.tilemaps.tilemap import TileMap


class GroupsPicker:
    def init(self, groups) -> None:
        self._groups: dict = groups

    def get_groups(self, *group_types) -> list[TileMap]:
        for type in group_types:
            if type not in self._groups.keys():
                raise InvalidGroupTypeError(f'{type} group does not exisit')
        sprite_groups = [self._groups[type] for type in group_types]
        return sprite_groups

    def get_group(self, type: GroupType) -> TileMap:
        return self._groups[type]


group_picker = GroupsPicker()
