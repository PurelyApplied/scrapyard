import logging
import random

from graph import Graph


def detect_component_sizes(g: Graph):
    logging.info("Attempting a recursive coloring...")
    def bleed(v, current, _colors):
        # print("bleed", current, "to", v)
        # print("Bleeding", current, "to", v)
        for n in g.edgelist[v]:
            # print("v", v, "has n", n)
            if _colors[n] is None:
                # print("bleed")
                _colors[n] = current
                bleed(n, current, _colors)
            elif _colors[n] != current and g.impose_symmetry:
                raise RuntimeError("Graph.detect_component_sizes:"
                                   " Impossible component crossing.")

    colors = {k: None for k in g.edgelist}
    current_color = 0
    for seed in list(colors.keys()):
        # print("try seed:", seed)
        if colors[seed] is None:
            colors[seed] = current_color
            bleed(seed, current_color, colors)
            current_color += 1
    return colors, current_color


def detect_component_sizes_non_recursive(g):
    logging.info("Determining component sizes for graph...")
    # Every node adopts the "color" of the minimum of their index and all neighbors.
    colors = {v: v for v in g.edgelist.keys()}
    any_change = True
    first_pass = True
    while any_change:
        logging.debug("Making a pass...")
        if not first_pass:
            logging.debug("Current colors: [{}]".format(sorted(list(set(colors.values())))))
        first_pass = False
        any_change = False
        for v in g.edgelist.keys():
            old = colors[v]
            colors[v] = min(colors[n] for n in g.edgelist[v])
            colors[v] = min(colors[v], old)
            if colors[v] != old:
                any_change = True
    return colors, len(set(colors.values()))


def get_degree_dist(g):
    dist = {}
    for v in g.edgelist.keys():
        d = len(g.edgelist[v])
        dist[d] = dist.get(d, 0) + 1
    return dist


def get_avg_deg(g, recompute=True):
    if recompute:
        g.determine_counts()
    avg_deg = g.m / g.n
    return avg_deg


def rmat_quality_experiment(n=100, k=11):
    edge_set = set()
    for i in range(n * k):
        left = random.randint(0, n - 2)
        right = random.randint(left + 1, n - 1)
        edge_set.add((left, right))
    print("Expected {} edges, actually got {}".format(n * k, len(edge_set)))
    isolated = {i for i in range(n)}
    for edge in edge_set:
        isolated -= set(edge)
    print("Isolated node count: {}".format(len(isolated)))


def draw_deg_dist(d, log_x=True, log_y=True):
    # These are the worst variable names.
    X = sorted(d.keys())
    Y = [d[x] for x in X]
    if log_x and log_y:
        plt.loglog(X, Y)
    elif log_x:
        plt.semilogx(X, Y)
    elif log_y:
        plt.semilogy(X, Y)
    else:
        plt.plot(X, Y)
    plt.title("Degree distribution")
    plt.show()


def prune_leaf_nodes(g: Graph):
    logging.info("Pruning leave edges from graph...")
    again = True
    while again:
        logging.debug("Looping...")
        again = False
        node_set = set(g.edgelist.keys())
        for n in node_set:
            if len(g[n]) == 1:
                logging.debug("Identified leaf node: {}".format(n))
                neigh = g[n][0]
                g[n].remove(neigh)
                if g.impose_symmetry:
                    g[neigh].remove(n)
                again = True
        for n in node_set:
            if len(g[n]) == 0:
                logging.debug("Removing node {}".format(n))
                g.edgelist.pop(n)
