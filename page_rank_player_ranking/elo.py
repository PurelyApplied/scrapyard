#!/usr/bin/env python3


def compute_elo_delta(player_a_elo, player_b_elo, player_a_score=1, k=32):
    """Returns the elo change *for player A*, given elo ratings for players A and B and *player A's* score."""
    return k * (player_a_score - expected_score(player_a_elo, player_b_elo))


def expected_score(player_a_elo, player_b_elo):
    """Returns the expected score *for player A*, given elo ratings for players A and B."""
    return _q(player_a_elo) / (_q(player_a_elo) + _q(player_b_elo))


def _q(elo):
    return pow(10, elo/400)

