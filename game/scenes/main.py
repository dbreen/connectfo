import pygame

from game import constants, gamestate, utils
from game.media import media
from game.scene import Scene


class MainScene(Scene):
    def setup(self, first_time=False):
        self.set_state('running', True)
        self.font = pygame.font.Font(constants.MENU_FONT, 20)
        self.win_font = pygame.font.Font(constants.MENU_FONT, 48)
        self.current_player = self.font.render("Current Player:", True, constants.BLACK)
        self.esc_for_menu = self.font.render("Press ESC for menu", True, constants.BLACK)
        self.stalemate = self.win_font.render("STALEMATE!!!", True, constants.BLACK)

    def render(self, screen):
        screen.blit(media['img.main_bg'], (0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # about button
        rect = self.about_rect()
        if rect.collidepoint(mouse_x, mouse_y):
            about = media['img.about_down']
        else:
            about = media['img.about']
        screen.blit(about, rect)

        # board
        self.draw_board(screen)

        winner = gamestate.board.winner
        if winner:
            center = utils.center(self.winner_text)
            screen.blit(self.winner_text, (center[0], 50))
            screen.blit(self.esc_for_menu, (20, 10))
        elif gamestate.board.full():
            center = utils.center(self.stalemate)
            screen.blit(self.stalemate, (center[0], 50))
            screen.blit(self.esc_for_menu, (20, 10))
        else:
            # current player
            screen.blit(self.current_player, (20, 10))
            current_color = constants.RED_TILE if gamestate.board.current_player == gamestate.RED else constants.YELLOW_TILE
            pygame.draw.circle(screen, current_color, (35 + self.current_player.get_width(), 20), 10)

            # current tile
            tile_x = mouse_x
            if tile_x  < constants.BOARD_LEFT + constants.TILE_SPACING:
                tile_x  = constants.BOARD_LEFT + constants.TILE_SPACING
            if (tile_x + constants.TILE_SIZE + constants.TILE_SPACING) > constants.BOARD_RIGHT:
                tile_x = constants.BOARD_RIGHT - (constants.TILE_SIZE + constants.TILE_SPACING)
            self.draw_tile(screen, current_color, (tile_x + constants.TILE_SIZE/2, 75))

            self.potential_x = max(0, min(int((tile_x - constants.BOARD_LEFT) / (constants.TILE_SIZE * 2 + constants.TILE_SPACING)), constants.TILES_ACROSS - 1))
            y = gamestate.board.next_spot(self.potential_x)
            if y is not None:
                pos = self.board_pos(self.potential_x, constants.TILES_DOWN - y - 1)
                pygame.draw.circle(screen, utils.lighten(current_color), pos, constants.TILE_SIZE / 2)

    def draw_board(self, screen):
        pygame.draw.rect(screen, constants.BOARD_BG, [constants.BOARD_LEFT, constants.BOARD_TOP, constants.BOARD_WIDTH, constants.BOARD_HEIGHT])
        for x, col in enumerate(gamestate.board.get_board()):
            for y, tile in enumerate(reversed(col)):
                if tile is gamestate.EMPTY:
                    color = constants.WHITE
                elif tile is gamestate.RED:
                    color = constants.RED_TILE
                else:
                    color = constants.YELLOW_TILE
                pos = self.board_pos(x, y)
                self.draw_tile(screen, color, pos)

    def board_pos(self, x, y):
        return (constants.BOARD_LEFT + x * (constants.TILE_SPACING + constants.TILE_SIZE * 2) + constants.TILE_SIZE + constants.TILE_SPACING,
               constants.BOARD_TOP + y * (constants.TILE_SPACING + constants.TILE_SIZE * 2) + constants.TILE_SIZE + constants.TILE_SPACING)

    def draw_tile(self, screen, color, pos):
        pygame.draw.circle(screen, color, pos, constants.TILE_SIZE)

    def about_rect(self):
        about = media['img.about']
        return pygame.Rect(670, 5, about.get_width(), about.get_height())

    def do_win(self):
        media['snd.win'].play()
        winner = gamestate.board.winner
        color = constants.RED_TILE if winner == gamestate.RED else constants.YELLOW_TILE
        self.winner_text = self.win_font.render("%s Wins!" % gamestate.board.player_name(winner), True, color)

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_scene('menu')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.about_rect().collidepoint(mouse_pos):
                self.manager.switch_scene('about')
                return True
            if not hasattr(self, 'potential_x'):
                return
            if not gamestate.board.winner:
                try:
                    gamestate.board.play(self.potential_x)
                except gamestate.ColumnFullError:
                    pass
                if gamestate.board.check_win():
                    self.do_win()
