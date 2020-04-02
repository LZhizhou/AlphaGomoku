from enum import Enum
import numpy as np

class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

def check_list_len_5_and_equal(lst):
    if len(lst) > 5:
        lst.pop(0)
    return len(lst) == 5 and all(x == lst[0] and x != Color.EMPTY.value for x in lst)
"""
represent the game as a numpy, handing the abstract logic of the game
"""

class Board:

    def __init__(self, size):
        self.size = size
        self.current_player = Color.BLACK
        self.board = np.zeros((self.size, self.size ), dtype=np.uint8)
        self.winner = None
        self.end = False

    def reset(self):
        self.current_player = Color.BLACK
        self.board = np.zeros((self.size , self.size ), dtype=np.uint8)
        self.winner = None
        self.end = False

    def play_stone(self, coord, color=None):
        if color is None:
            color = self.current_player
        if self.board[coord[1]][coord[0]] != color.EMPTY.value:
            return None
        self.board[coord[1]][coord[0]] = color.value
        self._check_for_win()
        self._switch_player()
        return color

    def _switch_player(self):
        if self.current_player == Color.BLACK:
            self.current_player = Color.WHITE
        else:
            self.current_player = Color.BLACK

    def _check_for_win(self):

        if np.count_nonzero(self.board) == self.size*self.size:
            self.end = True
            self.winner = None
        for row in range(self.size):
            horizontal_seq = []
            vertical_seq = []
            ascending_seq = []
            descending_seq = []
            symmetric_ascending_seq = []
            symmetric_descending_seq = []

            for col in range(self.size):
                horizontal_seq.append(self.board[row][col])
                vertical_seq.append(self.board[col][row])
                if row >= col:
                    ascending_seq.append(self.board[row - col][col])
                    symmetric_ascending_seq.append(self.board[col][row - col])
                if row + col < self.size:
                    descending_seq.append(self.board[row + col][col])
                    symmetric_descending_seq.append(self.board[col][row + col])

                if check_list_len_5_and_equal(horizontal_seq) or check_list_len_5_and_equal(vertical_seq) \
                        or check_list_len_5_and_equal(ascending_seq) \
                        or check_list_len_5_and_equal(descending_seq) \
                        or check_list_len_5_and_equal(symmetric_ascending_seq) \
                        or check_list_len_5_and_equal(symmetric_descending_seq):
                    self.end = True
                    # print(self.current_player)
                    self.winner = self.current_player
