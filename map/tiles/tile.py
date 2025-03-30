import pygame
from map.tiles.foundation import Foundation


class Tile(Foundation):
    class Sprite:
        def __init__(self, image: pygame.Surface, sort_y_offset: int = 0, **pos: tuple[int]) -> None:
            self.show = True
            self.flip = False
            self.angle = 0
            self._raw_image = image
            self._final_image = image
            self._rect: pygame.FRect = image.get_frect(**pos)
            self._rect_center = self._rect.center
            self._sort_y_offset = sort_y_offset
            self.render_offset = pygame.Vector2()

        def new_image(self, image):
            self._raw_image = image
            self._final_image = image

        def transform(self, angle=0, flip=(False, False), scale=1):
            transformed_image = pygame.transform.flip(self._raw_image, *flip)
            transformed_image = pygame.transform.rotate(transformed_image, angle)
            image_scale = (transformed_image.width * scale, transformed_image.height * scale)
            transformed_image = pygame.transform.scale(transformed_image, image_scale)
            self._rect = transformed_image.get_rect(center=self._rect_center)
            self._final_image = transformed_image
            self._angle = angle

        def update(self, hitbox_mid_bottom):
            self._rect.midbottom = hitbox_mid_bottom
            self._rect_center = self._rect.center

        @property
        def sort_y_offset(self): return self._sort_y_offset

        @property
        def image(self): return self._final_image

        @property
        def rect(self): return self._rect

    def __init__(self, groups, type: str, image: pygame.Surface, sort_y_offset: int = 0,
                 offgrid_tile: bool = False, z=5, special_flags=0, **pos: tuple[int]) -> None:

        self._sprite = self.Sprite(image, sort_y_offset, **pos)
        self.hitbox: pygame.FRect = image.get_frect(**pos)
        self._z = z
        self._special_flags = special_flags
        super().__init__(groups, type, offgrid_tile)

    # x
    def get_horizontal_collision(self, rect: pygame.FRect, collisions: set):
        return self.hitbox.colliderect(rect)

    # y
    def get_vertical_collision(self, rect: pygame.FRect, collisions: set):
        return self.hitbox.colliderect(rect)

    def horizontal_collision(self, entity, direction: pygame.Vector2):
        if direction.x > 0:
            entity.hitbox.right = self.hitbox.left
            entity.set_collision('right')
        elif direction.x < 0:
            entity.hitbox.left = self.hitbox.right
            entity.set_collision('left')

    def vertical_collision(self, entity, direction: pygame.Vector2):
        if direction.y > 0:
            entity.hitbox.bottom = self.hitbox.top
            entity.set_collision('bottom')
        elif direction.y < 0:
            entity.hitbox.top = self.hitbox.bottom
            entity.set_collision('top')

    @property
    def sprite(self) -> Sprite: return self._sprite

    @property
    def z(self): return self._z

    @property
    def special_flags(self): return self._special_flags

    def get_sprite(self):
        return (self._sprite.image, self._sprite.rect)
