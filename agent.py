import numpy as np
from board import Color
class AlphaGomoku:
    def __init__(self,board):
        self.board = board

    def get_move(self):
        return self.get_random_move()
    def get_random_move(self):
        moves = self.get_empty_moves()
        np.random.shuffle(moves)
        for i in moves:
            return (i[1],i[0])
        return None

    def get_empty_moves(self):
        return np.transpose(np.where(self.board.board==Color.EMPTY.value))