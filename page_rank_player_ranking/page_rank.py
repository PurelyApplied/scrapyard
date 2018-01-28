#!/usr/bin/env python3
import logging
import networkx as nx

from page_rank_player_ranking.player import Player

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
    pass


class MatchupHistory:
    next_identifier = 0
    DRAWS = "draws"

    def __init__(self, player1, player2, player1_wins, player2_wins, draws=0, identifier=None):
        self.player1 = player1
        self.player2 = player2
        self.wins = {player1: player1_wins, player2: player2_wins, MatchupHistory.DRAWS: draws}
        self.id = identifier if identifier is not None else MatchupHistory.iterate_id()

    @classmethod
    def iterate_id(cls):
        id_value = cls.next_identifier
        cls.next_identifier += 1
        return id_value

    def __getitem__(self, item):
        return self.wins[item]

    def __repr__(self):
        return (f"<MatchupHistory({self.player1}, {self.player2}, {self[self.player1]}, {self[self.player2]}, "
                f"{self[DRAWS]}, {self.id}>")

    def __str__(self):
        return f"<'{self.player1}' {self[self.player1]} - {self[self.player2]} '{self.player2}'>"

if __name__ == '__main__':
    logging.getLogger('').setLevel(logging.DEBUG)
    g = nx.Graph()
    g.add_node(1, {INFO: Player(1, 3), RANK: 0.5, PREV_RANK: 0.5})
    g.add_node(2, {INFO: Player(2, 3), RANK: 0.5, PREV_RANK: 0.5})
    g.add_node(3, {INFO: Player(3, 3), RANK: 0.5, PREV_RANK: 0.5})
    g.add_node("A", {INFO: Player("A", 1), RANK: 0.5, PREV_RANK: 0.5})

    g.add_weighted_edges_from([
        (1, "A", MatchupHistory(1, "A", 0, 1)),
        (1, 3, MatchupHistory(1, 3, 0, 1)),
        (2, 1, MatchupHistory(2, 1, 0, 1)),
        (2, 3, MatchupHistory(2, 3, 0, 1)),
        (3, 2, MatchupHistory(3, 2, 0, 1))], weight=MATCH_HISTORY)
    page_iteration(g)
    pass
