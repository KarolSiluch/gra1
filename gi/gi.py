from player.player import Player
import pygame


class GI():
    def __init__(self, context: Player):
        self._context = context

    def render(self, display: pygame.Surface):
        x, y = 10, display.get_height() - 15
        rect = pygame.Rect(x, y, 50 * self._context.charge_fraction, 5)
        pygame.draw.rect(display, '#0366fc', rect)
