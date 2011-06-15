import pygame

from game import gamestate, utils
from game.constants import *
from game.media import media
from game.scene import Scene


class MainScene(Scene):
    def load(self):
        # state variables
        self.set_state('running', True)
        self.drop_info = None

        # resources
        self.font = pygame.font.Font(MENU_FONT, 20)
        self.win_font = pygame.font.Font(MENU_FONT, 48)
        self.current_player = self.font.render("Current Player:", True, BLACK)
        self.esc_for_menu = self.font.render("Press ESC for menu, or N for a new game", True, BLACK)
        self.stalemate = self.win_font.render("STALEMATE!!!", True, BLACK)

    def render(self, screen):
        screen.blit(media['img.main_bg'], (0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        current_color = RED_TILE if gamestate.board.current_player == gamestate.RED else YELLOW_TILE

        # about button
        rect = self.about_rect()
        if rect.collidepoint(mouse_x, mouse_y):
            about = media['img.about_down']
        else:
            about = media['img.about']
        screen.blit(about, rect)

        winner = gamestate.board.winner
        if winner:
            center = utils.center(self.winner_text)
            screen.blit(self.winner_text, (center[0], 50))
            screen.blit(self.esc_for_menu, (20, 10))
        elif gamestate.board.full():
            center = utils.center(self.stalemate)
            screen.blit(self.stalemate, (center[0], 50))
            screen.blit(self.esc_for_menu, (20, 10))
        elif self.drop_info:
            # we're dropping a tile
            pos = self.board_pos(self.drop_info['col'], TILES_DOWN - self.drop_info['row'] - 1)
            self.drop_info['offset'] += TILE_DROP_SPEED
            y = self.drop_info['offset'] + BOARD_TOP - TILE_SIZE
            if y >= pos[1]:
                self.play_tile()
            else:
                x = BOARD_LEFT + TILE_SPACING + TILE_SIZE + self.drop_info['col'] * (TILE_SIZE * 2 + TILE_SPACING)
                self.draw_tile(screen, current_color, (x, y))
        else:
            # current player
            screen.blit(self.current_player, (20, 10))
            pygame.draw.circle(screen, current_color, (35 + self.current_player.get_width(), TILE_SIZE), 10)

            # current tile
            tile_x = mouse_x
            if tile_x  < BOARD_LEFT + TILE_SPACING:
                tile_x  = BOARD_LEFT + TILE_SPACING
            if (tile_x + TILE_SIZE + TILE_SPACING) > BOARD_RIGHT:
                tile_x = BOARD_RIGHT - (TILE_SIZE + TILE_SPACING)
            self.draw_tile(screen, current_color, (tile_x + TILE_SIZE/2, 75))

            # figure out which column is closest to the mouse position
            self.current_column = max(0, min(int((tile_x - BOARD_LEFT) / (TILE_SIZE * 2 + TILE_SPACING)), TILES_ACROSS - 1))
            y = gamestate.board.next_spot(self.current_column)
            if y is not None:
                pos = self.board_pos(self.current_column, TILES_DOWN - y - 1)
                pygame.draw.circle(screen, utils.lighten(current_color), pos, TILE_SIZE / 2)

        # board
        self.draw_board(screen)

    def draw_board(self, screen):
        board = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        board.set_colorkey(TRANSPARENT)
        board.fill(BOARD_BG)
        for x, col in enumerate(gamestate.board.get_board()):
            for y, tile in enumerate(reversed(col)):
                if tile is gamestate.EMPTY:
                    color = TRANSPARENT
                elif tile is gamestate.RED:
                    color = RED_TILE
                else:
                    color = YELLOW_TILE
                offset = TILE_SPACING + TILE_SIZE
                per_tile= (TILE_SPACING + TILE_SIZE * 2)
                pos = (offset + x * per_tile,
                       offset + y * per_tile)
                self.draw_tile(board, color, pos)
        screen.blit(board, (BOARD_LEFT, BOARD_TOP))

    def board_pos(self, x, y):
        return (BOARD_LEFT + x * (TILE_SPACING + TILE_SIZE * 2) + TILE_SIZE + TILE_SPACING,
               BOARD_TOP + y * (TILE_SPACING + TILE_SIZE * 2) + TILE_SIZE + TILE_SPACING)

    def draw_tile(self, screen, color, pos):
        pygame.draw.circle(screen, color, pos, TILE_SIZE)

    def about_rect(self):
        about = media['img.about']
        return pygame.Rect(670, 5, about.get_width(), about.get_height())

    def do_win(self):
        media['snd.win'].play()
        winner = gamestate.board.winner
        color = RED_TILE if winner == gamestate.RED else YELLOW_TILE
        self.winner_text = self.win_font.render("%s Wins!" % gamestate.board.player_name(winner), True, color)

    def drop_tile(self, current_column):
        self.drop_info = {
            'col': current_column,
            'row': gamestate.board.next_spot(self.current_column),
            'offset': 0
        }

    def play_tile(self):
        gamestate.board.play(self.drop_info['col'])
        self.drop_info = None
        if gamestate.board.check_win():
            self.do_win()
            return
        if gamestate.players.player_type() == gamestate.COMPUTER:
            self.drop_tile(gamestate.players.computer_move())
        if gamestate.board.check_win():
            self.do_win()

    def do_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_scene('menu')
            if gamestate.board.winner and event.key == pygame.K_n:
                gamestate.new_game(gamestate.players.red, gamestate.players.yellow)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.about_rect().collidepoint(mouse_pos):
                self.manager.switch_scene('about')
                return True
            if not hasattr(self, 'current_column') or self.drop_info:
                # If we're not over a column or are dropping a tile, don't let new plays happen
                return
            if not gamestate.board.winner:
                if gamestate.board.col_full(self.current_column):
                    # played tried to play on an empty column
                    pass
                else:
                    self.drop_tile(self.current_column)
