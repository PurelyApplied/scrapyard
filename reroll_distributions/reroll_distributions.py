#!/usr/bin/env python3
import argparse
import logging
from dataclasses import dataclass


def determine_distributions_stochastically():
    pass


def draw_distributions():
    pass


def report_distributions():
    pass


def main(args):
    logging.debug(f"Got args: {args}")
    logging.debug(f"Got policy {args.policy}")
    determine_distributions_stochastically()
    draw_distributions()
    report_distributions()


@dataclass
class Roll:
    initial_string: str


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--roll",
                        help="The base roll of dice to investigate.",
                        type=Roll,
                        required=True
                        )
    parser.add_argument("--reroll-count",
                        help="Number(s) to investigate for dice to reroll.",
                        type=int,
                        nargs="+",
                        default=[1, 2, 3, 4, 5],
                        required=True)
    parser.add_argument("--policy",
                        action='append',
                        nargs=2,
                        type=int,
                        metavar=('policy_die_size', 'policy_min_value'),
                        help="Pairs of numbers indicating die-size and lowest-reroll value, e.g., "
                             "'--policy 6 2 8 3' will reroll d6 with values 1 and 2 and d8 with values 1, 2, and 3",
                        required=True)

    _args = parser.parse_args()

    logging.getLogger().setLevel(logging.DEBUG)

    main(_args)
