from board.src import Constants
# Test for the Position class
from board.src.Position import Position


# Test the creation and modification of a position
def test_initial_position():
    initial_position = Position.initial_position()
    assert initial_position.red == Constants.RED
    assert initial_position.white == Constants.WHITE
    assert initial_position.kings == Constants.KINGS

    # All initial pieces are men
    assert initial_position.red_men() == Constants.RED
    assert initial_position.white_men() == Constants.WHITE

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

