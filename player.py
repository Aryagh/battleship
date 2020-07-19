from numpy.random import randint
from numpy import zeros, matrix, max
from typing import Any


class Player:
    def __init__(self, name=None):
        self.info = {'name': name, 'board': random_board_creator()}
        self.last_shot = None
        self.table = zeros([10, 10])
        self.true_table = zeros([10, 10])
        self.false_table = zeros([10, 10])
        self.probility_field = zeros([10, 10])
        self.four_is_hited = False
        self.three_is_hited = False
        self.two_is_hited = False
        self.shoot_number = 0

    def shoot(self):
        max_number = 0
        self.update_true_false_table()
        #print('true\n',self.true_table)
        #print('false\n', self.false_table)
        self.update_probility_field()
        #print(self.probility_field)
        for i in range(10):
            for j in range(10):
                if self.probility_field[i, j] == max(self.probility_field):
                    max_number += 1
        a = randint(0, max_number) + 1
        counter = 0
        #print(a,max_number,max(self.probility_field))
        for i in range(10):
            for j in range(10):
                if self.probility_field[i, j] == max(self.probility_field):
                    counter += 1
                if counter == a:
                    self.last_shot = [i, j]
                    self.shoot_number += 1
                    return self.last_shot

    def get_log(self, is_hit):
        if is_hit:
            self.true_table[self.last_shot[0], self.last_shot[1]] = 1
            self.table[self.last_shot[0], self.last_shot[1]] = 1
            #print(self.probility_field)
        else:
            self.false_table[self.last_shot[0], self.last_shot[1]] = 1
            self.table[self.last_shot[0], self.last_shot[1]] = -1
        #print(self.table)

    def reset_board(self):
        print (self.shoot_number)
        self.shoot_number = 0
        self.info['board'] = random_board_creator()
        self.true_table = zeros([10, 10])
        self.false_table = zeros([10, 10])
        self.table = zeros([10, 10])
        self.four_is_hited = False
        self.three_is_hited = False
        self.two_is_hited = False
        self.last_shot = None

    def update_probility_field(self, ships=(4, 3, 2, 1), board_size=10):
        self.probility_field = zeros([10, 10])
        for ship_length in ships:
            for x in range(10):
                for y in range(10):
                    # check if east side is open
                    if x + (ship_length - 1) <= board_size - 1:
                        if sum(self.false_table[x:x + ship_length, y]) == 0:
                            self.probility_field[x:x + ship_length, y] += 1 + sum(self.true_table[x:x + ship_length, y])*2

                    # check if south side is open
                    if y + (ship_length - 1) <= board_size - 1:
                        if sum(self.false_table[x, y:y + ship_length]) == 0:
                            self.probility_field[x, y:y + ship_length] += 1 + sum(self.true_table[x, y:y + ship_length])*2

    def update_true_false_table(self, board_size=10):
        if not self.four_is_hited:
            ship_length = 4
            for x in range(10):
                for y in range(10):
                    # check if east side is open
                    if x + (ship_length - 1) <= board_size - 1:
                        if sum(self.true_table[x:x + ship_length, y]) == ship_length:
                            self.true_table[x:x + ship_length, y] = 0
                            self.false_table[x:x + ship_length, y] = 1
                            self.four_is_hited = True

                    # check if south side is open
                    if y + (ship_length - 1) <= board_size - 1:
                        if sum(self.true_table[x, y:y + ship_length]) == ship_length:
                            self.true_table[x:x + ship_length, y] = 0
                            self.false_table[x:x + ship_length, y] = 1
                            self.four_is_hited = True
        elif not self.three_is_hited:
            if not self.four_is_hited:
                ship_length = 3
                for x in range(10):
                    for y in range(10):
                        # check if east side is open
                        if x + (ship_length - 1) <= board_size - 1:
                            if sum(self.true_table[x:x + ship_length, y]) == ship_length:
                                self.true_table[x:x + ship_length, y] = 0
                                self.false_table[x:x + ship_length, y] = 1
                                self.three_is_hited = True

                        # check if south side is open
                        if y + (ship_length - 1) <= board_size - 1:
                            if sum(self.true_table[x, y:y + ship_length]) == ship_length:
                                self.true_table[x:x + ship_length, y] = 0
                                self.false_table[x:x + ship_length, y] = 1
                                self.three_is_hited = True
        if self.four_is_hited and self.three_is_hited and not self.two_is_hited:
            ship_length = 2
            for x in range(10):
                for y in range(10):
                    # check if east side is open
                    if x + (ship_length - 1) <= board_size - 1:
                        if sum(self.true_table[x:x + ship_length, y]) == ship_length:
                            self.true_table[x:x + ship_length, y] = 0
                            self.false_table[x:x + ship_length, y] = 1
                            self.two_is_hited = True

                    # check if south side is open
                    if y + (ship_length - 1) <= board_size - 1:
                        if sum(self.true_table[x, y:y + ship_length]) == ship_length:
                            self.true_table[x:x + ship_length, y] = 0
                            self.false_table[x:x + ship_length, y] = 1
                            self.two_is_hited = True


def random_board_creator(board_size=10, ships=(4, 3, 2, 1)):
    board = zeros(shape=(10, 10))
    for ship_length in ships:
        ship_location = False
        while ship_location is False:
            (x, y) = randint(0, board_size, 2)
            orientation = []
            # check if north side is open
            if x - (ship_length - 1) >= 0:
                if sum(board[x - ship_length + 1:x + 1, y]) == 0:
                    orientation.append('north')
            # check if south side is open
            if x + (ship_length - 1) <= board_size - 1:
                if sum(board[x:x + ship_length, y]) == 0:
                    orientation.append('south')
            # check if east side is open
            if y + (ship_length - 1) <= board_size - 1:
                if sum(board[x, y:y + ship_length]) == 0:
                    orientation.append('east')
            # check if west side is open
            if y - (ship_length - 1) >= 0:
                if sum(board[x, y - ship_length + 1:y + 1]) == 0:
                    orientation.append('west')
            try:
                # there is a possible move
                assert len(orientation) != 0
                # pick a random orientation
                orient = orientation[randint(0, len(orientation))]
                if orient is 'north':
                    board[x - ship_length + 1:x + 1, y] = 1
                elif orient is 'south':
                    board[x:x + ship_length, y] = 1
                elif orient is 'east':
                    board[x, y:y + ship_length] = 1
                elif orient is 'west':
                    board[x, y - ship_length + 1:y + 1] = 1
                else:
                    raise ValueError
                ship_location = True
            except AssertionError:
                continue
    return matrix(board)
