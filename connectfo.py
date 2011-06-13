import pygame

from game import constants
from game.scene import SceneManager


def start_game():
    screen = pygame.display.set_mode(constants.SCREEN)
    clock = pygame.time.Clock()
    manager = SceneManager(screen, clock, constants.FPS)
    manager.run('menu')


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Connect Fo'")
    pygame.font.init()

    start_game()
