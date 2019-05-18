from board.src.Movement_Generator import MovementGenerator

# Test for the Movement Generator
def test_quiet_moves():
    quiet_moves = MovementGenerator.generate_quiet_moves()\

    assert sum(map(len, quiet_moves)) == 98