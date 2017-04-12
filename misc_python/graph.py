import random
import matplotlib.pyplot as plt
import os
from translation import Translation

class Graph:
    def __init__(self, in_edgelist=None, in_style=None,
                 symmetric=False, allow_loops=False, multiedge=False,
                 keep_sorted=False, keep_counts_updated=False, # <== both unused
                 node_type=str, start_ind=0):
        '''Will attempt to cast file-read edgelist to node_type.
        in_edgelist = filename or None
        in_style = 'edgelist'
        symmetric = True | False ; add_edge(a, b) also adds (b, a)
        multiedge = True | False ; allows multiple edges (a, b)
        node_type: attempts to cast key to associated type.
        start_ind: beginning presumed index in metis-style neighborlist'''
        # edgelist maps key element to sorted list of neighbors.
        self.symmetric = symmetric
        self.multiedge = multiedge
        self.allow_loops = allow_loops
        self.node_type = node_type
        self.keep_sorted = keep_sorted
        self.n, self.m = 0, 0
        self.translation = None # when collapsed, stored here for access
        
        self.edgelist = {}
        if in_edgelist and in_style:
            if in_style == "edgelist":
                self.load_from_edgelist(in_edgelist)
            else:
                raise RuntimeError(
                    "Graph only accepts in_style 'edgelist'")

    def __repr__(self):
        return "<Graph>"

    def __getitem__(self, i):
        return self.edgelist[i]

    def add_edge(self, a, b):
        if not self.multiedge and b in self.edgelist.get(a, []):
            return
        if not self.allow_loops and b == a:
            return
        self.edgelist[a] = self.edgelist.get(a, []) + [b]
        self.edgelist[b] = self.edgelist.get(b, [])
        if self.symmetric:
            self.edgelist[b] = self.edgelist[b] + [a]

    def detect_component_sizes(self):
        def bleed(v, current, colors):
            #print("bleed", current, "to", v)
            # print("Bleeding", current, "to", v)
            for n in self.edgelist[v]:
                #print("v", v, "has n", n)
                if colors[n] is None:
                    #print("bleed")
                    colors[n] = current
                    bleed(n, current, colors)
                elif colors[n] != current and self.symmetric:
                    raise RuntimeError("Graph.detect_component_sizes:"
                                       " Impossible component crossing.")
        colors = {k : None for k in self.edgelist}
        current_color = 0
        for seed in list(colors.keys()):
            # print("try seed:", seed)
            if colors[seed] is None:
                colors[seed] = current_color
                bleed(seed, current_color, colors)
                current_color += 1
        return colors, current_color

    def collapse_and_rename(self):
        '''Collapses names to ints and indexes 0 .. self.n-1'''
        translation = Translation(*self.edgelist.keys())
        new_edgelist = {}
        for u, neighbors in self.edgelist.items():
            new_edgelist[translation[u]] = [translation[v] for v in neighbors]
        self.edgelist = new_edgelist
        self.translation = translation
        self.translation.lock()
        
    def detect_component_sizes_non_recursive(self):
        # Every node adopts the "color" of the minimum of their index
        # and all neighbors.
        any_change = True
        colors = {v : v for v in self.edgelist.keys()}
        while any_change:
            any_change = False
            for v in self.edgelist.keys():
                old = colors[v]
                colors[v] = min(colors[n] for n in self.edgelist[v])
                if colors[v] != old:
                    any_change = True
        return colors

    def load_from_edgelist(self, filename):
        with open(filename) as f:
            i = 0
            for line in f:
                i += 1
                if not line.strip() or line.strip()[0] in "%#;":
                    continue
                assert len(line.split()) == 2,(
                    "Line %d (%s) is does not contain exactly two nodes."
                    % (i, line.strip()))
                source, target = line.split()
                if not isinstance(source, self.node_type):
                    source = self.node_type(source)
                if not isinstance(target, self.node_type):
                    target = self.node_type(target)
                self.add_edge(source, target)

    def has_edge(self, u, v):
        return v in self.edgelist.get(u, {})

    def get_properties_header(self):
        return ("# Graph properties:\n"
                "# n = {}; m = {}\n"
                "# Symmetric: {}\n"
                "# Multiedge: {}\n"
                "# Allow self loops: {}\n"
                .format(self.n if self.n else '?',
                        self.m if self.m else '?',
                        self.symmetric,
                        self.multiedge,
                        self.allow_loops))

    def write_edgelist(self, fileout, width=0, spacer=" ", header="",
                       index_offset=0):
        '''infer width on width=0'''
        width = width or max(len(str(k)) for k in self.edgelist)
        buff = ""
        if header:
            buff += "# " + header.strip().lstrip("#") + "\n#\n"
        buff += self.get_properties_header()
        fstr = "{{:{}}}".format(width)
        form = lambda x : fstr.format(x)
        for v in sorted(self.edgelist.keys()):
            for n in sorted(self.edgelist[v]):
                buff += spacer.join(map(form, (v, n))) + "\n"
        if fileout is None:
            print(buff)
        else:
            with open(fileout, 'w') as o:
                o.write(buff)

    def prune(self, duplicates=True, loops=True, isolated=True, sort=True,
              reevaluate_counts=False):
        for k in list(self.edgelist.keys()):
            if duplicates:
                self.edgelist[k] = set(self.edgelist[k])
            if loops:
                while k in self.edgelist[k]:
                    self.edgelist[k].remove(k)
            if not isinstance(self.edgelist[k], list):
                self.edgelist[k] = list(self.edgelist[k])
            if sort:
                self.edgelist[k].sort()
            if isolated and not self.edgelist[k]:
                del self.edgelist[k]
        if reevaluate_counts:
            self.determine_counts()

    def determine_counts(self):
        self.n = len(self.edgelist)
        self.m = sum(len(v) for _, v in self.edgelist.items())

    def count_duplicate_edges(self):
        dup = 0
        for v in self.edgelist:
            dup += len(self.edgelist[v]) - len(set(self.edgelist[v]))
        return dup

    def sort_edgelist(self):
        for k in list(self.edgelist.keys()):
            self.edgelist[k].sort()

    def get_degree_dist(self):
        dist = {}
        for v in self.edgelist.keys():
            d = len(self.edgelist[v])
            dist[d] = dist.get(d, 0) + 1
        return dist

    def get_avg_deg(self, recompute=True):
        if recompute:
            self.determine_counts()
        avg_deg = self.m / self.n
        return avg_deg

    # def load_from_metis(self, filename, starting_index=0):
    #     first_line_read = False
    #     with open(filename) as f:
    #         i = 0
    #         source = starting_index
    #         for line in f:
    #             i += 1
    #             # Blank lines are meaningful
    #             if not line.strip():
    #                 self.edgelist[self.node_type(source)] = []
    #                 source += 1
    #                 continue
    #             # Comments begin with % # or ;
    #             elif line.strip()[0] in "%#;":
    #                 continue
    #             elif not first_line_read:
    #                 self.n, self.m = (int(i) for i in line.split())
    #                 first_line_read = True
    #                 continue
    #             # Otherwise, we get a big list
    #             self.edgelist[self.node_type(source)] = [
    #                 self.node_type(t) for t in line.split()]
    #             source += 1
    # def write_metis(self, fileout, width=0, spacer=" ", header="",
    #                 recompute_header=True, index_offset=1):
    #     '''infer width on width=0'''
    #     width = width or max(len(str(k)) for k in self.edgelist)
    #     with open(fileout, 'w') as o:
    #         if recompute_header:
    #             self.determine_counts()
    #         if header:
    #             o.write("# " + header)
    #         o.write("%% First non-comment line represents: n m\n")
    #         o.write("%% Subsequent lines are 'neighbor lists.'\n")
    #         o.write("%% Indexing / first agent ID: {}\n".format(index_offset))
    #         o.write("{} {}\n".format(self.n, self.m))
    #         for i in range(self.n):
    #             o.write(spacer.join(
    #                 "{{:{}}}".format(width).format(str(n + index_offset))
    #                 for n in self.edgelist[i])
    #                 + "\n")


    






    
def draw_comm_sizes(G):
    colors, n_cols = G.detect_component_sizes()
    counts = [ sum(1 for k, v in colors.items() if v == i)
               for i in range(n_cols)]
    print(len(counts))
    print(len([c for c in counts if c > 1]))
    plt.semilogy()
    plt.ylim([0.01, 1000])
    plt.hist(counts)
    plt.show()

    
def rmat_qual_test(n=100, k=11):
    edgeset = set()
    for i in range(n * k):
        left = random.randint(0, n-2)
        right = random.randint(left+1, n-1)
        edgeset.add( (left, right))
    print("Edgected {} edges, actually got {}".format(n*k, len(edgeset)))
    isolated = {i for i in range(n)}
    for edge in edgeset:
        isolated -= set(edge)
    print("Isolated node count: {}".format(len(isolated)))

    
def draw_deg_dist(d, logx=True, logy=True):
    # These are the worst variable names.
    X = sorted(d.keys())
    Y = [d[x] for x in X]
    if logx and logy:
        plt.loglog(X, Y)
    elif logx:
        plt.semilogx(X, Y)
    elif logy:
        plt.semilogy(X, Y)
    else:
        plt.plot(X, Y)
    plt.title("Degree distribution")
    plt.show()
