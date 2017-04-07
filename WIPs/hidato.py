'''Hidato Solver, as proposed in /r/dailyprogrammer,
https://www.reddit.com/r/dailyprogrammer/comments/51wg0j/20160909_challenge_282_hard_hidato/
'''




class HidatoPuzzle:
    def __init__(self, bounding_size=(5, 5), holes=()):
        self.size = bounding_size
        self.tile = [[HidatoSpace((x, y))
                      for y in range(bounding_size[1])]
                     for x in range(bounding_size[0])]
        for x, y in holes:
            self.tile[x][y].hole=True
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                connect_to = [(x+i, y+j)
                              for i in (-1, 0, 1)
                              for j in (-1, 0, 1)
                              if (0 <= x + i < self.size[0]
                                  and 0 <= y + j < self.size[1]
                                  and (i or j))]
                print("Connect ({}, {}) to: {}".format(x, y, connect_to))
                for n_x, n_y in connect_to:
                    self.tile[x][y].add_neighbor(self.tile[n_x][n_y])

    def __repr__(self):
        return "<HidatoPuzzle>"

    def __str__(self):
        return "\n".join(
            " ".join(str(self.tile[x][y])
                     for x in range(self.size[0]))
            for y in range(self.size[1] -1, -1, -1))


class HidatoSpace:
    def __init__(self, pos, value=None, neighbors=None, hole=False):
        self.pos = pos
        self.value = value
        self.neighbors = set(neighbors) if neighbors else set()
        self.hole = hole
        # possible_values[i] = (value, imposing_source_value)
        self.possible_values = []

    def __repr__(self):
        return "<HidatoSpace: {}>".format(self.pos)

    def __str__(self):
        return (
            (self.value and "{:2d}".format(self.value))
            or (self.hole and "XX")
            or "__")

    def get_unsolved_neighbors_count(self):
        return sum(1 for i in self.neighbors if not i.value)

    def add_neighbor(self, other):
        self.neighbors.add(other)
        other.neighbors.add(self)


def get_empty_puzzle(size=(5, 5)):
    puzzle = [[HidatoSpace() for i in range(size[1])] for j in range(size[2])]
    connect_spaces(puzzle)
    return puzzle


def get_test_puzzle():
    p = HidatoPuzzle(holes=( (0,0), (0, 4), (4, 0), (4, 4)))
    p.tile[1][1].value = 1
    p.tile[1][2].value = 21
    return p


def connect_spaces(puzzle):
    pass


def render_puzzle(puzzle):
    pass # print("\n".join(


def solve(puzzle):
    pass


def read_puzzle(filename):
    pass


def str_to_puzzle(s):
    '''Format: __ for blank, XX for hole, value for known'''
    ll = [[str_to_space(i) for i in row.split()] for row in s.split("\n")]
    return ll


def str_to_space(s):
    return HidatoSpace(pos=None,
                       value=(int(s) if s.isnumeric() else None),
                       hole=(s == "XX"))

def get_test_str():
    return '''__  1 __ XX __
    __ __ __ __ __
    __ 14 __ __ __'''
    
def identify_isolated(puzzle):
    pass


def write(puzzle, position, number):
    pass






