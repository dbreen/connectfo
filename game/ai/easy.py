import random

from game import constants
from game.ai import AI


class EasyAI(AI):
    def make_move(self, board, me, them):
        highest = 0
        play = -1
        for col in range(constants.TILES_ACROSS):
            if board.col_full(col):
                continue
            val = self.max_for_col(board, board.board_state[me], col)
            if val > highest:
                highest = val
                play = col
        # Still haven't found a move... play a random non-full column
        if play == -1:
            cols = [col for col in range(constants.TILES_ACROSS)
                    if not board.col_full(col)]
            return random.choice(cols)
        return play
