import numpy as np

from board.src.Position import Position


class MovementGenerator:  # Class that generates all moves from each valid square

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

        attack_moves = []
        # Piece starting at square 1 (index 0)
        position = np.uint32(0x80000000)

        for i in range(0, 32):

            moves_from_square = []

            if Position.get_rank_from_index(i) == 1 or Position.get_rank_from_index(i) == 2:

                if Position.get_file_from_index(i) == 1 or Position.get_file_from_index(i) == 2:
                    moves_from_square.append(MovementGenerator.capture_north_east(position))

                elif Position.get_file_from_index(i) == 7 or Position.get_file_from_index(i) == 8:
                    moves_from_square.append(MovementGenerator.capture_north_west(position))

                else:
                    moves_from_square.append(MovementGenerator.capture_north_west(position))
                    moves_from_square.append(MovementGenerator.capture_north_east(position))

            elif Position.get_rank_from_index(i) == 7 or Position.get_rank_from_index(i) == 8:

                if Position.get_file_from_index(i) == 1 or Position.get_file_from_index(i) == 2:
                    moves_from_square.append(MovementGenerator.capture_south_east(position))

                elif Position.get_file_from_index(i) == 7 or Position.get_file_from_index(i) == 8:
                    moves_from_square.append(MovementGenerator.capture_south_west(position))

                else:
                    moves_from_square.append(MovementGenerator.capture_south_west(position))
                    moves_from_square.append(MovementGenerator.capture_south_east(position))

            else:
                if Position.get_file_from_index(i) == 1 or Position.get_file_from_index(i) == 2:
                    moves_from_square.append(MovementGenerator.capture_north_east(position))
                    moves_from_square.append(MovementGenerator.capture_south_east(position))

                elif Position.get_file_from_index(i) == 7 or Position.get_file_from_index(i) == 8:
                    moves_from_square.append(MovementGenerator.capture_north_west(position))
                    moves_from_square.append(MovementGenerator.capture_south_west(position))

                else:
                    moves_from_square.append(MovementGenerator.capture_north_east(position))
                    moves_from_square.append(MovementGenerator.capture_north_west(position))
                    moves_from_square.append(MovementGenerator.capture_south_west(position))
                    moves_from_square.append(MovementGenerator.capture_south_east(position))

            attack_moves.append(moves_from_square)
            position = np.uint32(position >> 1)  # Move to the next square

        return attack_moves

    # ------------------------------------------------------------------------------
    # Functions to perform a quiet/non-capture move
    #
    # Note: the odd_rank variable serves to adapt the shift of the moves between
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

    # ------------------------------------------------------------------------------
    # Functions to perform an attack/capture move
    #
    # ------------------------------------------------------------------------------
    @staticmethod
    def capture_north_east(position):
        return np.uint32(position | (position >> 7))

    @staticmethod
    def capture_north_west(position):
        return np.uint32(position | (position >> 9))

    @staticmethod
    def capture_south_east(position):
        return np.uint32(position | (position << 9))

    @staticmethod
    def capture_south_west(position):
        return np.uint32(position | (position << 7))
