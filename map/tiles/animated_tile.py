from map.tiles.tile import Tile
from animation.animation import Animation


class AnimatedTile(Tile):
    def __init__(self, groups, type: str, animations, first_state, render_y_offset: int = 0,
                 offgrid_tile: bool = False, **pos) -> None:

        self._animations = animations
        self._current_animation: Animation = self._animations[first_state].copy()
        super().__init__(groups, type, self._current_animation.img(), render_y_offset, offgrid_tile, **pos)

    @property
    def current_animation(self):
        return self._current_animation

    def animate(self):
        self.sprite.new_image(self._current_animation.img())

    def change_animation(self, state):
        self._current_animation = self._animations[state].copy()
