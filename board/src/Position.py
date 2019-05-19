import copy

import numpy as np

from board.src import Constants


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

    # ------------------------------------------------------------------------------
    # Functions to display a position
    # ------------------------------------------------------------------------------

    # Prints the given position
    def display_position(self):
        rk = self.red_kings()
        rm = self.red_men()
        wk = self.white_kings()
        wm = self.white_men()

        board = np.chararray((8, 8), 8, True)
        board[:] = '|__|'
        board = Position.fill_position(board, rm, Constants.RED_MAN)
        board = Position.fill_position(board, rk, Constants.RED_KING)
        board = Position.fill_position(board, wm, Constants.WHITE_MAN)
        board = Position.fill_position(board, wk, Constants.WHITE_KING)

        for rank in board[::-1]:
            print(' '.join(map(str, rank)))

    # Fills the board matrix based on the given bitboard and piece unicode code
    @staticmethod
    def fill_position(board, piece_bitboard: np.uint32, piece_type):
        index = 0
        for bit in np.binary_repr(piece_bitboard, 32):
            if bit == '1':
                rank = Position.get_rank_from_index(index)
                file = Position.get_file_from_index(index)
                board[rank][file] = "|{0}|".format(piece_type)
            index += 1

        return board

    # ------------------------------------------------------------------------------
    # Functions to execute a given move and update the position
    #
    # ------------------------------------------------------------------------------
    def execute_move(self, move, capture, player):

        # Get the bitboards of the origin and destination squares
        if player:
            origin = np.uint32(self.red & move)
        else:
            origin = np.uint32(self.white & move)

        destination = np.uint32(origin ^ move())

        # if not valid == 0. If capure -> bitboard of the captured piece
        relevant_bitboard = self.is_valid_move(origin, destination, capture, player)

        if relevant_bitboard:

            new_position = copy.deepcopy(self)

            # Update the player's bitboard
            if player:
                new_position.red = np.uint32(new_position.red ^ move)

            else:
                new_position.white = np.uint32(new_position.white ^ move)

            # Update the existing kings's bitboard, if needed
            if not (new_position.kings & move):  # 0 means that the piece moved was not a king
                new_position.kings = np.uint32(new_position.kings ^ move)

            # Check if there was a crowning
            self.check_crowning(new_position, destination, player)

            if capture:  # Remove piece from opponent's bitboard

                if player:
                    new_position.white = np.uint32(new_position.white ^ relevant_bitboard)

                else:
                    new_position.red = np.uint32(new_position.red ^ relevant_bitboard)

            return new_position

        return Constants.EMPTY_BOARD

    # If it is a capture, the returned value will be the bitboard of the captured piece
    def is_valid_move(self, origin, destination, capture, player):

        if player:
            bitboard = self.red
        else:
            bitboard = self.white

        # Check that destination is not occupied
        if bitboard & destination:

            if capture:  # Check that the captured piece is not ours
                captured = self.get_captured_piece(origin, destination)  # TODO get captured square

                if (self.red | self.white) & captured:  # There is a piece to capture

                    if player:
                        if self.white & captured:  # Check against white pieces
                            return captured
                    else:
                        if self.red & captured:  # Check against red pieces
                            return captured
        else:
            return 1

        return 0

    # Return the bitboard of the captured piece
    def get_captured_piece(self, origin, destination):
        captured = np.uint32(0x00000000)  # Bitboard of the captured piece
        return captured

    # Updates the new position if a crowning occurred
    def check_crowning(self, new_position, destination, player):

        # Check that the piece is not already a king
        if not new_position.kings & destination:

            if player:
                index = Position.find_index_of_less_significant_bit(destination)  # white's usually closer to LSB
                if Position.get_rank_from_index(index) == 8:
                    new_position.kings = new_position.kings | destination

            else:
                index = Position.find_index_of_most_significant_bit(destination)  # red's usually closer to MSB
                if Position.get_rank_from_index(index) == 1:
                    new_position.kings = new_position.kings | destination
