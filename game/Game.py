from board.src.Movement_Generator import MovementGenerator
from board.src.Position import Position

def main():
    position = Position.initial_position()
    position.display_position()


if __name__ == '__main__':
    main()
    quiet_moves = MovementGenerator.generate_quiet_moves()
    attack_moves = MovementGenerator.generate_attack_moves()
