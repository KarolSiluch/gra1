import pygame
from map.tiles.foundation import Foundation


class Tile(Foundation):
    class Sprite:
        def __init__(self, image: pygame.Surface, sort_y_offset: int = 0, **pos: tuple[int]) -> None:
            self.show = True
            self.flip = False
            self._raw_image = image
            self._final_image = image
            self._rect: pygame.FRect = image.get_frect(**pos)
            self._rect_center = self._rect.center
            self._angle = 0
            self._sort_y_offset = sort_y_offset
            self.render_offset = pygame.Vector2()

        def transform(self, angle=0, flip=(False, False), scale=1):
            transformed_image = pygame.transform.flip(self._raw_image, *flip)
            transformed_image = pygame.transform.rotate(transformed_image, angle)
            image_scale = (transformed_image.width * scale, transformed_image.height * scale)
            transformed_image = pygame.transform.scale(transformed_image, image_scale)
            self._rect = transformed_image.get_rect(center=self._rect_center)
            self._final_image = transformed_image
            self._angle = angle

        def ubdate(self, hitbox_center):
            self._rect.center = hitbox_center
            self._rect_center = hitbox_center

        @property
        def sort_y_offset(self): return self._sort_y_offset

        @property
        def image(self): return self._final_image

        @property
        def rect(self): return self._rect

    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0,
                 offgrid_tile: bool = False, z=5, special_flags=0, **pos: tuple[int]) -> None:
        # __init__ zajmował dużo miejsca, to zrobiłem linie odstępu, a komentaż jest po to, żeby flake8 się nie czepiał
        self._sprite = self.Sprite(image, sort_y_offset, **pos)
        self._hitbox: pygame.FRect = image.get_frect(**pos).inflate(0, -0.6 * image.get_height())
        self._z = z
        self._special_flags = special_flags
        super().__init__(groups, type, offgrid_tile)

    @property
    def sprite(self) -> Sprite: return self._sprite

    @property
    def hitbox(self) -> pygame.FRect: return self._hitbox

    @property
    def z(self): return self._z

    @property
    def special_flags(self): return self._special_flags

    def get_sprite(self):
        return (self._sprite.image, self._sprite.rect)

    def update(self, dt):
        self._sprite.ubdate(self._hitbox.center)
