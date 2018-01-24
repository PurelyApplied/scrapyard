#!/usr/bin/env python3
from fractions import Fraction
from pprint import pprint

from copy import deepcopy

import logging
from tabulate import tabulate

try:
    f = open("pythag.data")
except FileNotFoundError:
    f = open("../pythag.data")

# Form: k, m, n, a, b, c
PY_DATA = set(tuple(map(int, l.split())) for l in f if not l.startswith("#"))
f.close()

TRIPLES = tuple(d[3:] for d in PY_DATA)

PY_GRAPH = {}
for _k, _n, _m, _a, _b, _c in PY_DATA:
    PY_GRAPH[_a] = PY_GRAPH.get(_a, []) + [_b]
    PY_GRAPH[_a] = PY_GRAPH.get(_a, []) + [_c]
    PY_GRAPH[_b] = PY_GRAPH.get(_b, []) + [_a]
    PY_GRAPH[_b] = PY_GRAPH.get(_b, []) + [_c]
    PY_GRAPH[_c] = PY_GRAPH.get(_c, []) + [_a]
    PY_GRAPH[_c] = PY_GRAPH.get(_c, []) + [_b]


def get_top(graph):
    return sorted(PY_GRAPH.keys(), key=lambda k: len(PY_GRAPH[k]), reverse=True)


def get_disjoint_primitives(data, quit_at=None, sort=True):
    hit = set()
    goal = []
    if sort:
        data = sorted(data)
    for k, m, n, _, _, _ in data:
        if n not in hit and m not in hit:
            a = k * (m * m - n * n)
            b = 2 * k * n * m
            c = k * (m * m + n * n)
            hit.update({n, m})
            goal.append((a, b, c))
        if quit_at and len(goal) >= quit_at:
            return goal
    return goal


def validate(a, b, c):
    x = min((a, b, c))
    y = max((a, b, c))
    z = {a, b, c} - {x, y}
    z = next(iter(z))
    print(f"a = {x}\nb = {z}\nc = {y}")
    return y * y == x * x + z * z


def scaled(k, *args):
    return [k * a for a in args]


def drop(graph, n):
    logging.debug(f"To drop: {n}")
    logging.debug(f"Neighbors: {graph[n]}")
    for neighbor in graph[n]:
        logging.debug(f"  Neighbor: {neighbor}")
        logging.debug(f"  Neighbor's neighbors: {graph[neighbor]}")
        graph[neighbor].remove(n)
    graph.pop(n)


def k_centrality_pruning(g, k):
    graph = deepcopy(g)
    continue_prune = True
    while continue_prune:
        logging.debug("Pruning pass...")
        nodes = graph.keys()
        to_prune = [n for n in nodes if len(graph[n]) < k]
        continue_prune = bool(to_prune)
        for n in to_prune:
            drop(graph, n)
    return graph


if __name__ == "__main__":
    print(tabulate(get_disjoint_primitives(PY_DATA, 10)))
    # logging.getLogger('').setLevel(logging.DEBUG)
    g = k_centrality_pruning(PY_GRAPH, 4)
    print(f"Size of original graph: {len(PY_GRAPH)}")
    print(f"Size of reduced graph: {len(g)}")
