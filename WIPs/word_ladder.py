'''A word ladder builder.

Implemented as a depth-first searching algorithm.'''

from random import choice

class Node:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.neighbors = set()

    def __repr__(self):
        return "<Node: {}>".format(self.name)

    def connect_to(self, other, symmetric=True):
        self.neighbors.add(other)
        if symmetric:
            other.neighbors.add(self)


def load_dictionary(d_file):
    pass


def build_word_graph(word_list):
    pass


