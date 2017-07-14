#!/usr/bin/env python3
from functools import lru_cache
import itertools
import logging

from tabulate import tabulate
# noinspection PyUnresolvedReferences
from pprint import pprint

logging.getLogger('').setLevel(logging.DEBUG)

ALIVE = "X"
DEAD = "."


def main():
    pass


class World:
    def __init__(self, *live_cells, size=(10, 10), wrap_around=(False, False)):
        self.size = size
        self.wrap = wrap_around
        self.cells = [[None for x in range(size[1])] for y in range(size[0])]
        self.populate_cells()
        for x, y in live_cells:
            logging.debug("Initializing cell {},{} to live".format(x, y))
            self.cells[x][y].alive = True

    def _in_bounds(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def populate_cells(self):
        x = list(range(self.size[0]))
        y = list(range(self.size[1]))
        for i, j in itertools.product(x, y):
            self.cells[i][j] = Cell()
        for i, j in itertools.product(x, y):
            for di, dj in itertools.combinations((-1, 0, 1), 2):
                if di == dj == 0:
                    continue
                nx, ny = i + di, j + dj
                if self._in_bounds(nx, ny):
                    self.cells[i][j].add_neighbor(self.cells[nx][ny])

    def __repr__(self):
        return "<Conway World>"

    def __str__(self):
        return tabulate(self.cells)


class Cell:
    def __init__(self, alive=False, rule="B3/S23"):
        self.neighbors = set()
        self.alive = alive
        self.rule = Cell._rule_factory(rule)
        self.next_state = None

    @classmethod
    @lru_cache(maxsize=32)
    def _rule_factory(cls, rule):
        """Returns a function that returns the alive state for the next tick, as parsed from a rule string, 
        i.e. B3/S23 """
        bits = rule.split("/")
        assert len(bits) == 2, "Rule string {!r} does not adhere to Bab/Scd format".format(rule)

        def tick_rule(cell):
            n = sum(c.alive for c in cell.neighbors)
            if cell.alive:
                return n in (2, 3)
            return n in (3,)

        return tick_rule

    def add_neighbor(self, other):
        self.neighbors.add(other)
        other.neighbors.add(self)

    def __str__(self):
        return ALIVE if self.alive else DEAD

    def __repr__(self):
        return "<Cell: {}>".format('alive' if self.alive else 'dead')


if __name__ == "__main__":
    w = World((1, 1), (1, 2), (2, 1), (2, 2), size=(5, 5), wrap_around=(False, False), )
