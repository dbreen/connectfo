import pygame
import sys

from game import constants, gamestate
from game.ai.easy import EasyAI
from game.media import media
from game.scene import Scene

# List of menu options (text, action_method, condition) where condition is None or a callable.
# If it is a callable that returns False, the option is not shown.
CONTINUE = 0
NEW_GAME = 1
QUIT = 2
OPTIONS = [
    ('Continue', 'opt_continue', lambda scene: scene.game_running),
    ('2 Player', 'start_2_player', None),
    ('Vs CPU', 'start_vs_cpu', None),
    ('Computer Battle!', 'start_cpu_vs_cpu', None),
    ('Quit', 'opt_quit', None),
]

class MenuScene(Scene):
    def load(self):
        self.font = pygame.font.Font(constants.MENU_FONT, constants.MENU_FONT_SIZE)
        self.active_font = pygame.font.Font(constants.MENU_FONT, constants.MENU_FONT_SIZE_ACTIVE)
        media.play_music('intro')

    def setup(self, first_time=False):
        # Selected menu choice - if "Continue" is there, have that selected
        self._current_option = NEW_GAME if first_time else CONTINUE
        self.game_running = self.manager.get_state('main', 'running')

    def render_options(self, screen):
        x, y = 30, 30
        for index, (text, action, show) in enumerate(OPTIONS):
            if show is not None and not show(self):
                continue
            active = index == self._current_option
            font = self.active_font if active else self.font
            surf = font.render(text, True, constants.MENU_FONT_COLOR)
            screen.blit(surf, (x, y))
            if active:
                screen.blit(media['img.arrow'], (x - 25, y + 12))
            y += surf.get_height() + 10

    def render(self, screen):
        screen.blit(media['img.title'], (0, 0))
        self.render_options(screen)

    def opt_continue(self):
        self.manager.switch_scene('main')
        return True

    def new_match(self, player1, player2):
        media.fade_music(1000)
        gamestate.new_game(player1, player2)
        self.manager.switch_scene('main')
        return True

    def start_2_player(self):
        self.new_match(gamestate.HUMAN, gamestate.HUMAN)

    def start_vs_cpu(self):
        self.new_match(gamestate.HUMAN, EasyAI())

    def start_cpu_vs_cpu(self):
        self.new_match(EasyAI(), EasyAI())

    def opt_quit(self):
        sys.exit()

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if self.game_running:
                    self.manager.switch_scene('main')
                    return
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                media['snd.button'].play()
                move = -1 if event.key == pygame.K_UP else 1
                self._current_option = (self._current_option + move) % len(OPTIONS)
                if self._current_option == CONTINUE and not self.game_running:
                    self._current_option = NEW_GAME if event.key == pygame.K_DOWN else (len(OPTIONS) - 1)
            elif event.key == pygame.K_RETURN:
                if self._current_option != NEW_GAME:
                    media['snd.button_press'].play()
                action = OPTIONS[self._current_option][1]
                return getattr(self, action)()
        return False
