from game import constants


EMPTY = None
RED = 1
YELLOW = 2

class ColumnFullError(Exception):
    pass

class Board(object):
    def __init__(self):
        self.clear()

    def clear(self):
        self._player = RED
        self._winner = None
        self._board = self.init_board(lambda: EMPTY, constants.TILES_DOWN, constants.TILES_ACROSS)
        # Store counts of consecutive tiles as we're adding them. Pad each side by 1 to prevent
        # needing to bound-check. When a tile is played, add one to the largest consecutive value.
        # Values are tuples of (up-right diag, down-right diag)
        self._diags = {
            RED: self.init_board(lambda: [0, 0], constants.TILES_DOWN + 2, constants.TILES_ACROSS + 2),
            YELLOW: self.init_board(lambda: [0, 0], constants.TILES_DOWN + 2, constants.TILES_ACROSS + 2),
        }

    def init_board(self, val, rows, cols):
        return [[val() for row in range(0, rows)] for col in range(0, cols)]

    def play(self, col):
        column = self._board[col]
        for row in range(0, constants.TILES_ACROSS):
            if column[row] == EMPTY:
                break
            if row == constants.TILES_DOWN - 1:
                raise ColumnFullError
        column[row] = self._player

        self.do_diag(col+1, row+1, 0, 1, 1)
        self.do_diag(col+1, row+1, 1, 1, -1)

        self.change_player()

    def do_diag(self, col, row, index, dir1, dir2):
        """For this col/row check adjacent values in the specfied dir, updating each val by 1.
        If the val is >= our target consecutive value, flag the winner."""
        diag = self._diags[self._player]
        new_val = max(diag[col+dir1][row+dir2][index], diag[col-dir1][row-dir2][index]) + 1
        diag[col][row][index] = new_val
        # update adjacents with max val as well
        diag[col+dir1][row+dir2][index] = new_val
        diag[col-dir1][row-dir2][index] = new_val
        if new_val >= constants.NECESSARY_CONSEC:
            self._winner = self._player

    @property
    def current_player(self):
        return self._player

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

    def check_consec(self, vals):
        """If we find N consecutive non-empty values, return that repeated value"""
        last = EMPTY
        count = 0
        for val in vals:
            if val and (val == last or (val is not EMPTY and last is EMPTY)):
                count += 1
                if count == constants.NECESSARY_CONSEC:
                    self._winner = val
                    return
            else:
                count = 0
            last = val

    def check_win(self):
        for col in self._board:
            self.check_consec(col)
        for r in range(0, constants.TILES_DOWN):
            self.check_consec([row[r] for row in self._board])
        return self._winner is not EMPTY

    @property
    def winner(self):
        return self._winner

    def player_name(self, player):
        if player == RED:
            return "Red"
        else:
            return "Yellow"

    def print_board(self):
        chars = {EMPTY: 'O', RED: 'R', YELLOW: 'Y'}
        for col in self._board:
            for slot in col:
                print "%s " % chars[slot],
            print
        print
    
board = Board()

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
