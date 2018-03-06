#!/usr/bin/env python3
import logging
from typing import List

import networkx as nx

from page_rank_player_ranking.game_classes import Player, Match

INFO = 'info'
RANK = 'ranking'
PREV_RANK = 'previous-rank'

MATCH_HISTORY = 'history'
EDGE_WEIGHT = 'weight'
PREV_EDGE_WEIGHT = 'previous-weight'


def page_iteration(g: nx.Graph):
    """Copies  'weight' attr to 'previous' for all edges and nodes, and then performs page rank computation:
      N_weight = weighted sum of in edges' source node weights
    """
    for _, node_attributes in g.nodes(data=True):
        node_attributes[PREV_RANK] = node_attributes.get(RANK, 0.0)

    for _, __, edge_attributes in g.edges(data=True):
        edge_attributes[PREV_EDGE_WEIGHT] = edge_attributes.get(EDGE_WEIGHT, 0.0)

    for sink in g.nodes(data=False):
        logging.debug(f"(sink) Player '{sink}' info: {g.node[sink][INFO]}")
        g.node[sink][RANK] = 0.0

        for source in g[sink]:
            logging.debug(f"-- (source) Player '{source}' info: {g.node[source][INFO]}")
            logging.debug(f"-- Match history: {g[source][sink][MATCH_HISTORY]}")

            total_games = g.node[sink][INFO].games_played
            games_lost_to_sink = g[source][sink][MATCH_HISTORY][sink]
            g.node[sink][RANK] += g.node[source][PREV_RANK] * games_lost_to_sink / total_games


def match_to_edge(m: Match):
    """Match m between u and v to (u, v, m), as suitable for input to g.add_edge"""
    return m.player_a, m.player_b, m


def matches_to_edgelist(ms: List[Match]):
    return [match_to_edge(m) for m in ms]


if __name__ == '__main__':
    logging.getLogger('').setLevel(logging.DEBUG)
    g = nx.Graph()
    players = [Player(), Player(), Player(), Player()]
    g.add_nodes_from(players)
    matches = [
        Match(players[0], players[1], (1, 0)),
        Match(players[0], players[2], (1, 0)),
        Match(players[0], players[3], (1, 0)),
        Match(players[1], players[3], (1, 0)),
        Match(players[3], players[2], (1, 0)),
        ]
    g.add_weighted_edges_from(matches_to_edgelist(matches), weight=MATCH_HISTORY)

    page_iteration(g)
    pass
