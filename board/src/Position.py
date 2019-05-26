import copy

import numpy as np

from game import Constants


class Position:  # Class that represent a position of the game

    # ------------------------------------------------------------------------------
    # Functions for position set-up
    # ------------------------------------------------------------------------------

    # Populates a Position/State with the given position of the pieces
    def __init__(self, red, white, kings):
        # 3 uint32 Bitboards represent the complete state of the board
        self.red = red
        self.white = white
        self.kings = kings

    @staticmethod
    def initial_position():
        return Position(Constants.INITIAL_REDS, Constants.INITIAL_WHITES, Constants.INITIAL_KINGS)

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
        return (index // 4) + 1

    @staticmethod
    def get_file_from_index(index):
        return (7 - ((index % 4) * 2) - ((index // 4 + 1) % 2)) + 1

    @staticmethod
    def find_index_of_less_significant_bit(position):

        n = copy.deepcopy(position)
        count = 0
        while (n):
            n = n >> 1
            count += 1

        return 32 - count

    @staticmethod
    def find_index_of_most_significant_bit(position):

        n = copy.deepcopy(position)
        count = 0
        while (n):
            n = n << 1
            count += 1

        return count

    @staticmethod
    def get_bitboard_from_index(index):

        position = copy.deepcopy(Constants.MSB_SET)
        for x in range(index):
            position = position >> 1

        return position

    # ------------------------------------------------------------------------------
    # Functions to display a position
    # ------------------------------------------------------------------------------
    # Prints the given position on the console
    def display_position(self):
        rk = self.red_kings()
        rm = self.red_men()
        wk = self.white_kings()
        wm = self.white_men()

        board = np.chararray((8, 8), 8, True)
        board[:] = '|__|'
        board = Position.fill_position(board, rm, Constants.RED_MAN_UNICODE)
        board = Position.fill_position(board, rk, Constants.RED_KING_UNICODE)
        board = Position.fill_position(board, wm, Constants.WHITE_MAN_UNICODE)
        board = Position.fill_position(board, wk, Constants.WHITE_KING_UNICODE)

        for rank in board[::-1]:
            print(' '.join(map(str, rank)))

    # Fills the board matrix based on the given bitboard and piece unicode code
    @staticmethod
    def fill_position(board, piece_bitboard: np.uint32, piece_unicode):
        index = 0
        for bit in np.binary_repr(piece_bitboard, 32):
            if bit == '1':
                rank = Position.get_rank_from_index(index) - 1
                file = Position.get_file_from_index(index) - 1
                board[rank][file] = "|{0}|".format(piece_unicode)
            index += 1

        return board

    # ------------------------------------------------------------------------------
    # Functions to execute a given move and update the position
    #
    # ------------------------------------------------------------------------------
    def execute_move(self, move, is_capture, captured, player):

        # Get the bitboards of the origin and destination squares
        origin = np.uint32(self.red & move) if player else np.uint32(self.white & move)
        destination = np.uint32(origin ^ move)

        # if not valid == 0
        if self.is_valid_move(destination, is_capture, captured, player):

            new_position = copy.deepcopy(self)

            # Whole Color
            if player:
                new_position.red = np.uint32(new_position.red ^ move)
            else:
                new_position.white = np.uint32(new_position.white ^ move)

            # Kings
            if new_position.kings & move:  # 0 means the piece moved was not a king
                new_position.kings = np.uint32(new_position.kings ^ move)

            # Update opponent's bitboards
            if is_capture:
                if player:
                    new_position.white = np.uint32(new_position.white ^ captured)
                else:
                    new_position.red = np.uint32(new_position.red ^ captured)

            # Check and perform crowning
            self.check_crowning(new_position, destination, player)

            return new_position

        return Constants.EMPTY_BOARD

    # If it is a capture, the returned value will be the bitboard of the captured piece
    def is_valid_move(self, destination, is_capture, captured, player):

        board = self.white ^ self.red

        # Check that destination is not occupied
        if not board & destination:  # 0 == free square

            if is_capture:  # Check that the captured piece is not ours

                if board & captured:  # There is a piece to captures
                    if player:  # Red
                        if self.white & captured:  # Check against white pieces
                            return 1
                    else:
                        if self.red & captured:  # Check against red pieces
                            return 1
            else:
                return 1

        return 0

    # Updates the new position if a crowning occurred
    @staticmethod
    def check_crowning(new_position, destination, player):

        # piece is not already a king
        if not new_position.kings & destination:
            if player:  # Red
                index = Position.find_index_of_less_significant_bit(destination)  # white is  closer to LSB
                if Position.get_rank_from_index(index) == 8:
                    new_position.kings = new_position.kings | destination

            else:
                index = Position.find_index_of_most_significant_bit(destination)  # red is closer to MSB
                if Position.get_rank_from_index(index) == 1:
                    new_position.kings = new_position.kings | destination
