import numpy as np

from board.src import Constants


class Position:  # Class representing the state of the board

    # ------------------------------------------------------------------------------
    # Functions for position set-up
    # ------------------------------------------------------------------------------

    # Creates a Position/State with the given position of the pieces
    def __init__(self, red, white, kings):
        # 3 uint32 Bitboards represent the complete state of the board
        self.red = red
        self.white = white
        self.kings = kings

    # Returns the initial position of the game
    @staticmethod
    def initial_position():
        return Position(Constants.RED, Constants.WHITE, Constants.KINGS)

    # ------------------------------------------------------------------------------
    # Functions to obtain the position of the pieces
    # ------------------------------------------------------------------------------

    # Returns all red kings
    def red_kings(self):
        return self.red & self.kings

    # Returns all red men
    def red_men(self):
        return self.red & ~self.kings

    # Returns all white kings
    def white_kings(self):
        return self.white & self.kings

    # Returns all white men
    def white_men(self):
        return self.white & ~self.kings

    # ------------------------------------------------------------------------------
    # Functions to translate between square  and bitboard indexes
    # ------------------------------------------------------------------------------
    @staticmethod
    def get_rank_from_index(index):
        return index // 4

    @staticmethod
    def get_file_from_index(index):
        return 7 - ((index % 4) * 2) - ((index // 4 + 1) % 2)

    # ------------------------------------------------------------------------------
    # Functions to move a piece
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # Functions to display a position
    # ------------------------------------------------------------------------------

    # Prints the given position
    def display_board(self):
        rk = self.red_kings()
        rm = self.red_men()
        wk = self.white_kings()
        wm = self.white_men()

        board = np.chararray((8, 8), 8, True)
        board[:] = '|__|'
        board = Position.fill_board(board, rm, Constants.RED_MAN)
        board = Position.fill_board(board, rk, Constants.RED_KING)
        board = Position.fill_board(board, wm, Constants.WHITE_MAN)
        board = Position.fill_board(board, wk, Constants.WHITE_KING)

        for rank in board[::-1]:
            print(' '.join(map(str, rank)))

    # Fills the board matrix based on the given bitboard and piece unicode code
    @staticmethod
    def fill_board(board, piece_bitboard: np.uint32, piece_type):
        index = 0
        for bit in np.binary_repr(piece_bitboard, 32):
            if bit == '1':
                rank = Position.get_rank_from_index(index)
                file = Position.get_file_from_index(index)
                board[rank][file] = "|{0}|".format(piece_type)
            index += 1

        return board
