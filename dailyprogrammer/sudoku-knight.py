#!/usr/bin/env python3
"""
/r/DailyProgrammer challenge posed at
https://www.reddit.com/r/dailyprogrammer/comments/8ked11/20180518_challenge_361_hard_sudoku_knights_tour/

Summary: given a (valid, solved) Sudoku, find the maximal knight tour using the utility
  sum_i( 10^(81 - i) e_i)
where i is the index of the knight's tour and e_i is the value of the cell the knight occupies in that step.

Alternatively, produce the largest value knight's tour if the knight writes one number, copying the cell value en route.

====

This solution is a modified DFS.
While such an approach would generally be intractable, we employ the following optimiztaions:
- We verify at each stem that a valid knight's tour remains possible
--- There exist at most 1 degree 1 node remaining, excluding the currently occupied node
--- There exists only one connected component
- We prioritize high value cells, so that the first valid knight's tour found will be of maximal value.
--- Some care is taken to note potential ties (undetermined)
"""
from pprint import pprint
from typing import List

import networkx as nx
from itertools import product as powerset
import logging
from prettytable import PrettyTable
from enum import Enum

logging.getLogger().setLevel(logging.DEBUG)


class NodeAttr(str, Enum):
    cell_value = "cell"


class SudokuGraph(nx.Graph):
    def __init__(self, entries: List[List[int]] = None):
        edges = []
        deltas = self._knight_deltas()
        logging.debug(f"Deltas: f{deltas}")
        for y, x, (dy, dx) in powerset(range(9), range(9), self._knight_deltas()):
            # For symmetry, we choose to only wire positive dy
            y_less_ydy = y < y + dy
            xdx_in_range = x + dx in range(9)
            ydy_in_range = y + dy in range(9)
            if y_less_ydy or not xdx_in_range or not ydy_in_range:
                logging.debug(f"Skipping ({x}, {y}) -- ({x + dx}, {y + dy}) ;"
                              f"y<ydy: {y_less_ydy}; xdx not in: {not xdx_in_range}; yxy not in: {not ydy_in_range}")
                pass
            else:
                edges.append(((x, y), (x + dx, y + dy)))
                logging.debug(f"Adding {(x, y)} -- {(x + dx, y + dy)}")

        super().__init__(edges)
        if entries:
            for y, x in powerset(range(9), range(9)):
                self.nodes[(x, y)][NodeAttr.cell_value] = entries[y][x]

    @staticmethod
    def _knight_deltas():
        return sorted([
            ((sx * x), (sy * (3 - x))) for x, sx, sy in powerset((1, 2), (1, -1), (1, -1))
        ])

    def as_table(self):
        table = PrettyTable(border=False, header=False)
        data = [[self.node[(x, y)][NodeAttr.cell_value] for x in range(9)] for y in range(9)]
        for row in data:
            table.add_row(row)
        return table


def solve(g):
    sorted_nodes = sorted(g.nodes().keys(), key=lambda n: -g.node[n][NodeAttr.cell_value])
    print(g.as_table())
    pprint(sorted_nodes)


def main(source):
    g = SudokuGraph(source)
    get_and_assert_on_degree_distribution(g)
    get_and_assert_table_cell_data_matches_expectation(g)
    solve(g)


def get_and_assert_table_cell_data_matches_expectation(g):
    actual = [[int(i) for i in l.strip().split()] for l in str(g.as_table()).strip().split("\n")]
    expected = test_source()
    logging.debug("Actual:")
    logging.debug(f"{actual}")
    logging.debug("Expected:")
    logging.debug(f"{expected}")
    assert expected == actual


def get_and_assert_on_degree_distribution(g: SudokuGraph):
    deg_dist = {i: 0 for i in range(2, 9)}
    for node in g.nodes():
        neighbors = list(g.neighbors(node))
        deg = len(neighbors)
        logging.debug(f"Node {node} has degree {deg} with neighbors: {neighbors}")
        deg_dist[deg] += 1
    logging.debug("Actual:")
    logging.debug(", ".join(f"deg {k} : {v}" for k, v in deg_dist.items()))
    assert_deg_dist = {2: 4,
                       3: 8,
                       4: 3 * 4 + (9 - 6) * 4,
                       5: 0,
                       6: 3 * 4 + (9 - 6) * 4 - 4,
                       7: 0,
                       8: (9 - 4) * (9 - 4)}
    logging.debug("Should be:")
    logging.debug(", ".join(f"deg {k} : {v}" for k, v in assert_deg_dist.items()))
    assert deg_dist == assert_deg_dist, "Actual degree distribution does not match expectation."


def test_source():
    source = ("1 6 4 8 2 7 3 5 9\n"
              "7 5 3 6 9 4 8 2 1\n" 
              "8 2 9 1 5 3 4 7 6\n" 
              "6 4 7 3 1 9 2 8 5\n" 
              "3 9 5 2 4 8 6 1 7\n" 
              "2 1 8 7 6 5 9 3 4\n" 
              "9 7 1 4 8 2 5 6 3\n" 
              "4 8 6 5 3 1 7 9 2\n"
              "5 3 2 9 7 6 1 4 8")
    return [[int(i) for i in l.strip().split()] for l in source.strip().split("\n")]




if __name__ == '__main__':
    main(test_source())
