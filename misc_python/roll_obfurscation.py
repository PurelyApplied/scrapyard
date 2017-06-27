#!/usr/bin/env python3
from random import shuffle
from tabulate import tabulate


def main(keep_crits=False):
    source = list(range(1, 21))
    if keep_crits:
        source.remove(1)
        source.remove(20)
    targets = source.copy()
    shuffle(targets)
    adjustments = {s: t for t, s in zip(targets, source)}
    if keep_crits:
        adjustments[1] = 1
        adjustments[20] = 20

    print(tabulate(sorted((x, adj, "{:+3d}".format(adj - x)) for x, adj in adjustments.items()),
                   headers=("Roll", "Adjusted", "Delta"),
                   stralign='left',
                   numalign='left'))

if __name__ == "__main__":
    main()
