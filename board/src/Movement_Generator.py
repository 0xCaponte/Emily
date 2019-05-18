import numpy as np

from board.src.Position import Position


class MovementGenerator:  # Class that generates all movements from each valid square

    # ------------------------------------------------------------------------------
    # Generate all moves from all squares
    # ------------------------------------------------------------------------------
    @staticmethod
    def generate_quiet_moves():  # non-captures

        quiet_moves = []
        # Piece starting at square 1 (index 0)
        position = np.uint32(0x80000000)

        for i in range(0, 32):

            moves_from_square = []

            if Position.get_rank_from_index(i) == 1:  # Bottom rank
                moves_from_square.append(
                    MovementGenerator.move_north_east(position, (Position.get_rank_from_index(i) % 2)))

                if i != 3:  # not bottom left corner
                    moves_from_square.append(
                        MovementGenerator.move_north_west(position, (Position.get_rank_from_index(i) % 2)))

            elif Position.get_rank_from_index(i) == 8:  # Top rank
                moves_from_square.append(
                    MovementGenerator.move_south_west(position, (Position.get_rank_from_index(i) % 2)))

                if i != 28:  # not top right corner
                    moves_from_square.append(
                        MovementGenerator.move_south_east(position, (Position.get_rank_from_index(i) % 2)))

            elif Position.get_file_from_index(i) == 1:  # Leftmost file
                moves_from_square.append(
                    MovementGenerator.move_north_east(position, (Position.get_rank_from_index(i) % 2)))
                moves_from_square.append(
                    MovementGenerator.move_south_east(position, (Position.get_rank_from_index(i) % 2)))

            elif Position.get_file_from_index(i) == 8:  # Rightmost file
                moves_from_square.append(
                    MovementGenerator.move_north_west(position, (Position.get_rank_from_index(i) % 2)))
                moves_from_square.append(
                    MovementGenerator.move_south_west(position, (Position.get_rank_from_index(i) % 2)))

            else:  # All squares not on the border of the board
                moves_from_square.append(
                    MovementGenerator.move_north_west(position, (Position.get_rank_from_index(i) % 2)))
                moves_from_square.append(
                    MovementGenerator.move_north_east(position, (Position.get_rank_from_index(i) % 2)))
                moves_from_square.append(
                    MovementGenerator.move_south_west(position, (Position.get_rank_from_index(i) % 2)))
                moves_from_square.append(
                    MovementGenerator.move_south_east(position, (Position.get_rank_from_index(i) % 2)))

            quiet_moves.append(moves_from_square)
            position = np.uint32(position >> 1)  # Move to the next square

        return quiet_moves

    @staticmethod
    def generate_attack_moves():  # captures
        pass

    # ------------------------------------------------------------------------------
    # Functions to move a piece
    #
    # Note: the odd_rank variable serves to adapt the shift of the movements between
    # ranks.
    # ------------------------------------------------------------------------------
    @staticmethod
    def move_north_east(position, odd_rank):
        shift = 3 + odd_rank
        return np.uint32(position | (position >> shift))

    @staticmethod
    def move_north_west(position, odd_rank):
        shift = 4 + odd_rank
        return np.uint32(position | (position >> shift))

    @staticmethod
    def move_south_east(position, odd_rank):

        shift = 5 - odd_rank
        return np.uint32(position | (position << shift))

    @staticmethod
    def move_south_west(position, odd_rank):
        shift = 4 - odd_rank
        return np.uint32(position | (position << shift))

    @staticmethod
    def print_moves(moves):

        for i in range(0, 32):

            print("From square = {}".format(i))

            # TODO Remember that the move has from and to. I just want the To
            # Front == i
            for move in moves[i]:
                move[i] = 0
                print("\t To Square 1 = {}".format(move.bit_length - 1))
                print("\t To Square 2 = {}".format(int(np.math.log(move, 2)) + 1))

        print(moves)
