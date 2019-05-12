from board.src import Constants
from board.src.Position import Position


# Test for the Position class
def test_initial_position():

    initial_position = Position.initial_position()
    assert initial_position.red == Constants.RED
    assert initial_position.white == Constants.WHITE
    assert initial_position.kings == Constants.KINGS