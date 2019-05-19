from board.src.Movement_Generator import MovementGenerator

# Tests the Movement Generator
def test_quiet_moves():
    quiet_moves = MovementGenerator.generate_quiet_moves()
    assert sum(map(len, quiet_moves)) == 98

def test_attack_moves():
    attack_moves = MovementGenerator.generate_attack_moves()
    assert sum(map(len, attack_moves)) == 72

