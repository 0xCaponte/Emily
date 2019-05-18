from board.src import Constants

# Test for the Position class
from board.src.Position import Position


def test_initial_position():
    initial_position = Position.initial_position()
    assert initial_position.red == Constants.RED
    assert initial_position.white == Constants.WHITE
    assert initial_position.kings == Constants.KINGS
