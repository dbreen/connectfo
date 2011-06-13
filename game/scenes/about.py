import pygame
import random

from game import constants
from game.media import media
from game.scene import Scene


class Bouncy(object):
    def __init__(self, surf):
        self.surf = surf
        self.pos_x = random.randrange(0, constants.SCREEN_WIDTH - surf.get_width())
        self.pos_y = random.randrange(0, constants.SCREEN_HEIGHT - surf.get_height())
        self.vel_x = random.randrange(2, 8)
        self.vel_y = random.randrange(2, 8)

    def update(self):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        if self.pos_x < 0:
            self.pos_x = 0
            self.vel_x = -self.vel_x
        if self.pos_y < 0:
            self.pos_y = 0
            self.vel_y = -self.vel_y
        if self.pos_x + self.surf.get_width() >= constants.SCREEN_WIDTH:
            self.pos_x = constants.SCREEN_WIDTH - self.surf.get_width() - 1
            self.vel_x = -self.vel_x
        if self.pos_y + self.surf.get_height() >= constants.SCREEN_HEIGHT:
            self.pos_y = constants.SCREEN_HEIGHT - self.surf.get_height() - 1
            self.vel_y = -self.vel_y

    def draw(self, screen):
        screen.blit(self.surf, (self.pos_x, self.pos_y))

class AboutScene(Scene):
    def load(self):
        font = pygame.font.Font(constants.MENU_FONT, 36)
        self.bouncers = [Bouncy(font.render("Dan is better than Matt!!", True, constants.WHITE))]
        for i in range(0, 5):
            self.bouncers.append(Bouncy(media[random.choice(['img.dragon1', 'img.dragon2'])]))

    def render(self, screen):
        screen.fill(constants.BLACK)
        for bouncer in self.bouncers:
            bouncer.update()
            bouncer.draw(screen)

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_scene('main')
