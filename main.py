import pygame
from time import time
from game_loops.loop import Loop
from game_loops.gameplay_loop import GameplayLoop


def Render_Text(screen: pygame.Surface, what: str, color: str, where: tuple[int]) -> None:
    font = pygame.font.Font(None, 30)
    text = font.render(what, True, pygame.Color(color))
    screen.blit(text, where)


class Main:
    def __init__(self) -> None:
        pygame.init()
        self._running: bool = True
        self._clock: pygame.Clock = pygame.time.Clock()
        self._previous_time = time()

        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        flags = pygame.FULLSCREEN | pygame.SCALED
        self._screen: pygame. Surface = pygame.display.set_mode((screen_size[0] // 3, screen_size[1] // 3), flags)
        self.loops = {
            'gameplay': GameplayLoop(self),
        }
        self._current_loop: Loop = self.loops['gameplay']

    def close(self) -> None:
        self._running = False

    def main_loop(self):
        while self._running:
            self._clock.tick(300)
            dt = time() - self._previous_time
            self._previous_time = time()
            self._current_loop.get_events()
            self._current_loop.update(dt)
            self._current_loop.render(self._screen)
            Render_Text(self._screen, str(int(self._clock.get_fps())), '#ffbb00', (self._screen.width - 40, 3))
            pygame.display.update()


if __name__ == '__main__':
    Main().main_loop()
