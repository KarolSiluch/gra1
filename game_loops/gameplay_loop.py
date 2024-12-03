import pygame
from game_loops.loop import Loop
from gameplay.gameplay import Gameplay


class GameplayLoop(Loop):
    def __init__(self, game) -> None:
        self._game = game
        self._gameplay = Gameplay()
        self._events = {}
        self.reset_events()

    @property
    def gameplay(self):
        return self._gameplay

    def enter(self):
        self.reset_events()

    def reset_events(self):
        for button in ['w', 'a', 's', 'd', 'e', 'mouse1', 'mouse3', 'shift', 'q', 'space']:
            self._events[button] = False

    def update(self, dt):
        self._gameplay.update(dt, self._events)

    def render(self, display: pygame.Surface):
        display.fill('#07123a')
        self._gameplay.render(display)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self._events['w'] = True
                if event.key == pygame.K_a:
                    self._events['a'] = True
                if event.key == pygame.K_s:
                    self._events['s'] = True
                if event.key == pygame.K_d:
                    self._events['d'] = True
                if event.key == pygame.K_LSHIFT:
                    self._events['shift'] = True
                if event.key == pygame.K_e:
                    self._events['e'] = True
                if event.key == pygame.K_q:
                    self._events['q'] = True
                if event.key == pygame.K_SPACE:
                    self._events['space'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self._events['w'] = False
                if event.key == pygame.K_a:
                    self._events['a'] = False
                if event.key == pygame.K_s:
                    self._events['s'] = False
                if event.key == pygame.K_d:
                    self._events['d'] = False
                if event.key == pygame.K_LSHIFT:
                    self._events['shift'] = False
                if event.key == pygame.K_q:
                    self._events['q'] = False
                if event.key == pygame.K_SPACE:
                    self._events['space'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._events['mouse1'] = True
                if event.button == 3:
                    self._events['mouse3'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self._events['mouse1'] = False
