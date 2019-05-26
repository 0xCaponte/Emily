# Test for the Position class
from board.src.Position import Position
from game import Constants


# Test the creation and modification of a position
def test_initial_position():
    initial_position = Position.initial_position()
    assert initial_position.red == Constants.INITIAL_REDS
    assert initial_position.white == Constants.INITIAL_WHITES
    assert initial_position.kings == Constants.INITIAL_KINGS

    # All initial pieces are men
    assert initial_position.red_men() == Constants.INITIAL_REDS
    assert initial_position.white_men() == Constants.INITIAL_WHITES

# def test_moves_from_initial_position():
#     initial_position = Position.initial_position()
#     quiet_moves = MovementGenerator.generate_quiet_moves()
#     attack_moves = MovementGenerator.generate_attack_moves()
#
#     possible_positions = []
#     # Execute and test moves for piece at square 11 at initial position
#     for move in quiet_moves[10]:  # Movement for piece at square 11
#         new_position = initial_position.execute_movement(move, Constants.RED_PLAYER)
#         possible_positions.append(new_position)

