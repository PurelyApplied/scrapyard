#!/usr/bin/env python3
import argparse
import logging
import random
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt


@dataclass
class Die:
    die_size: int
    last_roll: int = None

    def roll(self):
        self.last_roll = random.randint(1, self.die_size)
        return self.last_roll

    def __int__(self):
        return self.last_roll or 0


@dataclass
class Dice:
    dice: List[Die]

    def roll(self):
        for d in self.dice:
            d.roll()
        return sum(d.last_roll for d in self.dice)


class DiceDistribution:
    pass


def determine_distributions_stochastically():
    pass


def draw_distributions():
    plt.plot()
    pass


def report_distributions():
    pass


def main(args):
    logging.debug(f"Got args: {args}")
    logging.debug(f"Got policy {args.policy}")
    determine_distributions_stochastically()
    draw_distributions()
    report_distributions()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--dice",
                        action='append',
                        nargs=2,
                        type=int,
                        metavar=('die_size', 'die_count'),
                        help="Pairs of numbers indicating die-size and number of the specified die size, e.g., "
                             "'--dice 6 2' will roll 2d6.",
                        required=True)
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
