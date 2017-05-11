import random


# Partition, Community are just sets.
# GroundTruth is a list of sets
# noinspection SpellCheckingInspection
class Partitioning:
    def __init__(self, filename=None):
        """self.part maps [thread] -> set of agents"""
        self.vert_to_part = {}
        self.part = {}
        if filename:
            self.load_from_file(filename)

    def __repr__(self):
        return "<Partitioning ({})>".format(len(self))

    def __str__(self):
        return "  ".join(
            "p {} : {}".format(i, len(self.part[i]))
            for i in range(len(self.part)))

    def __len__(self):
        return len(self.part)

    def __iter__(self):
        return iter(self.part.values())

    def __getitem__(self, key):
        return self.part[key]

    def load_from_file(self, filename):
        """Loads a partitioning from the given file.  Expects the format
<name> <tag> <partition>.  <tag> is discarded.  Ignores empty lines
and any line beginning with [#;%], ignoring leading whitespace.

        """
        with open(filename) as f:
            for line in f:
                if not line.strip() or line.strip()[0] in "#;%":
                    continue
                v, _, p = map(int, line.split())
                self.vert_to_part[v] = p
        for v, p in self.vert_to_part.items():
            if p not in self.part:
                self.part[p] = set()
            self.part[p].add(v)

    def generate_random(self, n, k):
        self.part = {i: set() for i in range(k)}
        for i in range(n):
            self.part[random.randint(0, k - 1)].add(i)

    def generate_bias_random(self, n, bias=0.5):
        self.part = {i: set() for i in range(2)}
        for i in range(n):
            self.part[int(random.random() > bias)].add(i)

    def vertices(self):
        return len(self.vert_to_part) or sum(len(v) for v in self.part.values())

    def compare(self, other):
        changes = {}
        for v in self.vert_to_part.keys():
            if self.vert_to_part[v] != other.vert_to_part[v]:
                changes[v] = (self.vert_to_part[v], other.vert_to_part[v])
        return changes

    def load_from_sets(self, set_list):
        for i, s in enumerate(set_list):
            self.part[i] = s
            for v in s:
                self.vert_to_part[v] = s
