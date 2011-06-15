

class AI(object):
    def make_move(self, board, me, them):
        pass

    def max_for_col(self, board, repr, col):
        """Returns the max consecutive val, regardless of direction"""
        next_spot = board.next_spot(col)
        highest = 0
        for i in range(4):
            to_check = repr[i][col+1][next_spot+1]
            if to_check > highest:
                highest = to_check
        return highest
    