class Foundation:
    def __init__(self, groups, tile_type: str, offgrid_tile: bool = False) -> None:
        self._g = {}
        self._tile_type = tile_type
        self._offgrid_tile = offgrid_tile
        self._add_to_groups__(groups, offgrid_tile)

    @property
    def tile_type(self):
        return self._tile_type

    @property
    def offgrid_tile(self):
        return self._offgrid_tile

    def _add_to_groups__(self, groups: list, offgrid_tile: bool) -> None:
        for group in groups:
            place = group.add(self, offgrid_tile)
            self._g[group] = place

    def kill(self):
        for group, place in self._g.items():
            group.remove_internal(self, place)
