import random


class BoardGenerator(object):
    def __init__(self, x, y, difficulty=5, target_start=(2, 0), target_end=(2, 1)):
        self.x = x
        self.y = y
        self.target_y = target_start[0]
        self.difficulty = difficulty
        self.board = self.initialize_board(target_start, target_end)
        self.number_of_cars = 0

        self.generate_horizontal_cars()
        self.generate_vertical_cars()

    def initialize_board(self, start, end):
        board = [[None for _ in range(self.x)] for _ in range(self.y)]
        board[start[0]][start[1]] = 'r'
        board[end[0]][end[1]] = 'r'
        return board

    def generate_horizontal_cars(self):
        for y in range(self.y):
            for x in range(self.x-1):
                if self.number_of_cars == 9:
                    break

                if y == self.target_y:
                    continue

                if self.board[y][x] is not None:
                    continue

                if random.randrange(0, 10) > self.difficulty * 0.6:
                    continue

                if self.board[y][x+1] is None:
                    self.board[y][x] = str(self.number_of_cars)
                    self.board[y][x+1] = str(self.number_of_cars)
                    if x+2 <= self.x-1 and self.board[y][x+2] is None:
                        if random.randrange(0, 10) > self.difficulty:
                            self.board[y][x+2] = str(self.number_of_cars)

                    self.number_of_cars += 1

    def generate_vertical_cars(self):
        for x in range(self.x):
            for y in range(self.y-1):
                if self.number_of_cars == 9:
                    break

                if self.board[y][x] is not None:
                    continue

                if random.randrange(0, 10) > self.difficulty* 0.6:
                    continue

                if self.board[y+1][x] is None:
                    self.board[y][x] = str(self.number_of_cars)
                    self.board[y+1][x] = str(self.number_of_cars)

                    if y+2 <= self.y-1 and self.board[y+2][x] is None:
                        if random.randrange(0, 10) > self.difficulty:
                            self.board[y+2][x] = str(self.number_of_cars)

                    self.number_of_cars += 1

    def board_to_string(self):
        string = ""
        for row in self.board:
            for elem in row:
                if elem is None:
                    string += '.'
                else:
                    string += elem
            string += '\n'
        return string.rstrip()



