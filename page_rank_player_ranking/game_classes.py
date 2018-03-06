#!/usr/bin/env python3
from page_rank_player_ranking.utils import retained, generated


@generated
@retained
class Match:
    def __init__(self, player_a, player_b, score: tuple):
        self.player_a = player_a
        self.player_b = player_b
        self.score = score
        if player_a > player_b:
            self._flip_order()

    def _flip_order(self):
        self.player_a, self.player_b = self.player_b, self.player_a
        self.score = (self.score[1], self.score[0])

    def __repr__(self):
        return f"<Match({self.player_a}, {self.player_b}, {self.score})>"


@generated
@retained
class Player:
    def __init__(self, identifier=None):
        self.id = identifier if identifier is not None else Player.get_identifier()

    def __repr__(self):
        return f"<Player(identifier={self.id}>"

    def __lt__(self, other):
        return self.id < other.id

    @classmethod
    def get_identifier(cls):
        identifier = cls.next_identifier
        cls.next_identifier += 1
        return identifier


class PlayerRating:
    def __init__(self, player):
        self.player = player

if __name__ == '__main__':
    for _ in range(100):
        Player()
    for i in range(100):
        print(Player.get_instance(i)._get_generated_id())
