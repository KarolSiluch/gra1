import pygame


class InGameMouse:
    def __init__(self) -> None:
        self._cursor = pygame.Vector2()

    def update(self, offset: pygame.Vector2):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._coursor = pygame.Vector2(offset.x + mouse_x, offset.y + mouse_y)

    def mouse_vector(self, point) -> pygame.Vector2:
        point_x, point_y = point
        return pygame.Vector2(self._coursor.x - point_x, self._coursor.y - point_y)

    def get_pos(self) -> tuple[int]:
        return tuple(self._coursor)


cursor = InGameMouse()
