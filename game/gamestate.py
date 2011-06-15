from game import constants
from game.ai import AI


EMPTY = None
RED = 1
YELLOW = 2

HUMAN = 1
COMPUTER = 2

# Give offsets on how to move around the board when checking for consecutive tiles
DIRS = (
    [1, 0], [0, 1], # up, and down
    [1, 1], [-1, 1] # diagonals
)

class ColumnFullError(Exception):
    pass

class Board(object):
    def __init__(self):
        self.clear()

    def clear(self):
        self._player = RED
        self._winner = EMPTY
        self._board = self.init_board(EMPTY, constants.TILES_DOWN, constants.TILES_ACROSS)
        # Store counts of consecutive tiles as we're adding them. Pad each side by 1 to prevent
        # needing to bound-check. When a tile is played, add one to the largest consecutive value.
        # Values are tuples with the number of consecutive tiles in each direction (up, down, two diags)
        self._tilerep = {}
        for player in (RED, YELLOW):
            self._tilerep[player] = []
            for dir in DIRS:
                self._tilerep[player].append(self.init_board(0, constants.TILES_DOWN + 2, constants.TILES_ACROSS + 2))

    def init_board(self, val, rows, cols):
        return [[val for row in range(0, rows)] for col in range(0, cols)]

    def col_full(self, col):
        return not any(slot is EMPTY for slot in self._board[col])

    def play(self, col):
        column = self._board[col]
        for row in range(0, constants.TILES_ACROSS):
            if column[row] == EMPTY:
                break
            if row == constants.TILES_DOWN - 1:
                raise ColumnFullError
        column[row] = self._player

        # add to the consecutive tiles representation for each direction
        for i, dir in enumerate(DIRS):
            self.update_repr(col+1, row+1, i, dir[0], dir[1])

        self.change_player()

    def update_repr(self, col, row, dir, dir1, dir2):
        """For this col/row check adjacent values in the specfied dir, updating each val by 1.
        If the val is >= our target consecutive value, flag the winner."""
        repr = self._tilerep[self._player][dir]
        new_val = repr[col+dir1][row+dir2] + repr[col-dir1][row-dir2] + 1
        repr[col][row] = new_val
        # update adjacents with max val as well, if they have a tile
        if repr[col+dir1][row+dir2] > 0:
            repr[col+dir1][row+dir2] = new_val
        if repr[col-dir1][row-dir2] > 0:
            repr[col-dir1][row-dir2] = new_val
        if new_val >= constants.NECESSARY_CONSEC:
            self._winner = self._player
            print "Winning board values:"
            self.print_board(repr)

    @property
    def board_state(self):
        return self._tilerep

    @property
    def current_player(self):
        return self._player

    @property
    def other_player(self):
        return YELLOW if self._player == RED else YELLOW

    def change_player(self):
        self._player = RED if self._player == YELLOW else YELLOW

    def full(self):
        return all(all(slot != EMPTY for slot in col) for col in self._board)

    def get_board(self):
        return self._board

    def next_spot(self, col):
        for row, slot in enumerate(self._board[col]):
            if slot == EMPTY:
                return row
        return None

    def check_win(self):
        return self._winner is not EMPTY

    @property
    def winner(self):
        return self._winner

    def player_name(self, player):
        if player == RED:
            return "Red"
        else:
            return "Yellow"

    def print_board(self, board=None):
        if board is None:
            board = self._board
        for col in board:
            for slot in col:
                print "%d " % slot,
            print
        print
    
board = Board()

class Players(object):
    def start(self, red, yellow):
        self._players = {
            RED: red, YELLOW: yellow
        }

    @property
    def red(self):
        return self._players[RED]

    @property
    def yellow(self):
        return self._players[YELLOW]

    def computer_move(self):
        ai = self._players[board.current_player]
        return ai.make_move(board, board.current_player, board.other_player)

    def player_type(self):
        """Return the type of player whose turn it is now"""
        player = self._players[board.current_player]
        if isinstance(player, AI):
            return COMPUTER
        else:
            return HUMAN

players = Players()

def new_game(red, yellow):
    board.clear()
    players.start(red, yellow)

if __name__ == "__main__":
    board.print_board()
    board.play(1)
    board.play(1)
    board.play(0)
    board.play(0)
    board.play(0)
    board.play(0)
    board.play(0)
    board.play(0)
    board.play(3)
    board.play(6)
    board.print_board()
