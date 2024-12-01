import pygame


class Gameplay:
    def update(self, dt, events): ...

    def render(self, display: pygame.Surface): ...
