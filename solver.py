from copy import deepcopy

VERTICAL = 'vertical'
HORIZONTAL = 'horizontal'


class CannotSolveException(Exception):
    pass


class Car(object):
    def __init__(self, orientation, is_target, start, end, id):
        self.orientation = orientation
        self.is_target = is_target
        self.start = start
        self.end = end
        self.id = id

    def can_move(self, direction, matrix):
        if self.orientation == HORIZONTAL:
            if direction in ['up', 'down']:
                return False

            if direction == 'left':
                if self.start['x'] <= 0 or matrix[self.start['y']][self.start['x']-1] != '.':
                    return False
            else:  # right
                if self.end['x'] >= len(matrix[0])-1 or matrix[self.end['y']][self.end['x']+1] != '.':
                    return False

        else:  # VERTICAL
            if direction in ['left', 'right']:
                return False

            if direction == 'up':
                if self.start['y'] <= 0 or matrix[self.start['y']-1][self.start['x']] != '.':
                    return False
            else:  # down
                if self.end['y'] >= len(matrix)-1 or matrix[self.end['y']+1][self.end['x']] != '.':
                    return False
        return True

    def move(self, direction, length):
        if direction == 'up':
            self.start['y'] -= length
            self.end['y'] -= length

        if direction == 'down':
            self.start['y'] += length
            self.end['y'] += length

        if direction == 'left':
            self.start['x'] -= length
            self.end['x'] -= length

        if direction == 'right':
            self.start['x'] += length
            self.end['x'] += length


class Board(object):
    def __init__(self, board_data):
        self.size = {'x': len(board_data.lstrip().splitlines()[0]), 'y': len(board_data.lstrip().splitlines())}
        self.cars = self.generate_cars(board_data.lstrip())

    def generate_cars(self, board_data):
        board_data = board_data.splitlines()
        cars = self.generate_horizontal_cars(board_data) + self.generate_vertical_cars(board_data)
        return cars

    def generate_horizontal_cars(self, board_data):
        cars = []
        for x in range(self.size['y']):
            car_model = '.'
            for y in range(self.size['x']):
                item = board_data[x][y]
                if item != '.':
                    if item != car_model:
                        car_model = board_data[x][y]
                    elif item == car_model:
                        if y == self.size['y']-1 or board_data[x][y+1] != car_model:
                            cars.append(Car(
                                HORIZONTAL,
                                car_model == 'r',
                                {'x': y - 1, 'y': x},
                                {'x': y, 'y': x},
                                car_model))
                        else:
                            cars.append(Car(
                                HORIZONTAL,
                                car_model == 'r',
                                {'x': y - 1, 'y': x},
                                {'x': y + 1, 'y': x},
                                car_model))
                        car_model = '.'
        for car in cars:
            print(f"start:({car.start['x']}, {car.start['y']}) end:({car.end['x']}, {car.end['y']}) id: {car.id}")
        return cars

    def generate_vertical_cars(self, board_data):
        cars = []
        for x in range(self.size['x']):
            car_model = '.'
            for y in range(self.size['y']):
                item = board_data[y][x]
                if item != '.':
                    if item != car_model:
                        car_model = board_data[y][x]
                    elif item == car_model:
                        if y >= self.size['y'] - 1 or board_data[y+1][x] != car_model:
                            cars.append(Car(
                                VERTICAL,
                                car_model == 'r',
                                {'x': x, 'y': y - 1},
                                {'x': x, 'y': y},
                                car_model))
                        else:
                            cars.append(Car(
                                VERTICAL,
                                car_model == 'r',
                                {'x': x, 'y': y - 1},
                                {'x': x, 'y': y + 1},
                                car_model))
                        car_model = '.'
        for car in cars:
            print(f"start:({car.start['x']}, {car.start['y']}) end:({car.end['x']}, {car.end['y']}) id: {car.id}")
        return cars

    def solve(self):
        visited = set()
        q = [[[], self.cars]]

        while len(q) != 0:
            moves, cars = q.pop(0)

            if self.is_solved(cars):
                return moves

            for new_moves, new_cars, matrix in self.get_all_boards(cars):
                h = ""
                for m in self.cars_to_string_data(new_cars):
                    h += "".join(map(str, m))

                if hash(h) not in visited:
                    q.append([moves + new_moves, new_cars])
                    visited.add(hash(h))

        raise CannotSolveException

    def get_all_boards(self, cars):
        states = []
        matrix = self.cars_to_string_data(cars)
        for car in cars:
            for direction in ['up', 'down', 'left', 'right']:
                if car.can_move(direction, matrix):
                    new_cars = deepcopy(cars)
                    new_car = next(filter(
                        lambda x: x.id == car.id, new_cars))
                    new_car.move(direction, 1)
                    states.append([[[car.id, direction]], new_cars, matrix])

                    #for m in self.cars_to_string_data(new_cars):
                    #   print(m)
                    #print()

        return states

    def is_solved(self, cars):
        target = next(filter(lambda x: x.is_target, cars))
        if target.end['x'] == self.size['x'] - 1:
            return True
        return False

    def cars_to_string_data(self, cars):
        matrix = [['.' for _ in range(self.size['x'])] for _ in range(self.size['y'])]
        for car in cars:
            if car.orientation == HORIZONTAL:
                for i in range(car.start['x'], car.end['x']+1):
                    matrix[car.start['y']][i] = car.id
            else:
                for i in range(car.start['y'], car.end['y']+1):
                    matrix[i][car.start['x']] = car.id
        return matrix


