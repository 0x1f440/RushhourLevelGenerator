from board_generator import *
from solver import *

if __name__ == '__main__':
    number_of_levels = 10
    minimum_moves = 6  # If it is 4, some level will have no blocks beside rr block.

    with open('sample_output.txt', mode='a') as csv_file:
        counter = 0
        while counter < number_of_levels:
            try:
                board_data = BoardGenerator(6, 6, 5).board_to_string()
                moves = Board(board_data).solve()
                if len(moves) >= minimum_moves:
                    csv_file.write(board_data + ",\n")
                    counter += 1
                    print("new map appended...")

            except CannotSolveException:
                print("cannot solve...")
                pass

    print("map generation ended...")
