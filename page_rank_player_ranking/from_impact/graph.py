import logging
import time

from translation import Translation


class Graph:
    def __init__(self, in_edgelist=None, in_style=None,
                 impose_symmetry=False, allow_loops=False, allow_multiedge=False,
                 permissive=True, clean=True, node_type=str):
        """Will attempt to cast file-read edgelist to node_type.
        in_edgelist = filename or None
        in_style = 'edgelist' # Safeguard against old METIS usage.

        symmetric = True | False ; add_edge(a, b) also adds (b, a)
        multiedge = True | False ; allows multiple edges (a, b)
        allow_loops = True | False ; allows edge (a, a)

        node_type: attempts to cast key to associated type.
        permissive: attempting to add an illegal edge proceeds quietly; raises an exception when False
        clean: prunes isolated nodes and translates all nodes to a zero-indexing

        Every node will be present in the edgelist's keys.  This includes a node in a directed graph with no out-edges.

        Symmetric flag does not grant memory savings, but explicitly saves (v,u) for each (u,v) added."""
        # edgelist maps key element to sorted list of neighbors.
        self.source_edgelist = in_edgelist
        self.impose_symmetry = impose_symmetry
        self.allow_multiedge = allow_multiedge
        self.allow_loops = allow_loops
        self.permissive = permissive
        self.node_type = node_type
        self.n, self.m = 0, 0
        self.translation = None  # when collapsed, stored here for access

        self.edgelist = {}
        if in_edgelist and in_style:
            if in_style == "edgelist":
                self.load_from_edgelist(in_edgelist)
            else:
                raise RuntimeError(
                    "Graph only accepts in_style 'edgelist'")
        if clean:
            self.prune(duplicates=False, loops=False, isolated=True, sort=True,
                       reevaluate_counts=True)
            self.collapse_and_rename()

    def __repr__(self):
        return "<Graph>"

    def __getitem__(self, i):
        return self.edgelist[i]

    def _check_potential_edge(self, a, b):
        violations = []
        if not self.allow_multiedge and b in self.edgelist.get(a, []):
            violations.append("Edge exists but multiedge set to false")
        if not self.allow_loops and b == a:
            violations.append("Loops disallowed")
        if self.impose_symmetry and (not self.allow_multiedge and a in self.edgelist.get(b, [])):
            violations.append("Symmetric edge exists but multiedge set to false")
        return violations

    def add_edge(self, a, b, insert_as='list'):
        """insert_as is a hack: accept 'list' or 'set'"""
        if self._check_potential_edge(a, b):
            if self.permissive:
                return
            else:
                raise InvalidEdgeException(
                    "Cannot add edge ({}, {}): {}".format(a, b, "; ".join(self._check_potential_edge(a, b))))
        if insert_as == 'list':
            self.edgelist[a] = self.edgelist.get(a, []) + [b]
            self.edgelist[b] = self.edgelist.get(b, [])
            if self.impose_symmetry:
                self.edgelist[b] = self.edgelist[b] + [a]
        elif insert_as == 'set':
            self.edgelist[a].add(b)
            if self.impose_symmetry:
                self.edgelist[b].add(a)
        else:
            raise RuntimeError("You were an idiot once, and now you're paying for it.")

    def impose_symmetry(self, update_flag=True):
        """Adds edge (v,u) for every edge (u,v) in a non-symmetric graph."""
        assert not self.impose_symmetry, "Graph has symmetric flag set."
        agents = set(self.edgelist.keys())
        for u in agents:
            for v in self.edgelist[u]:
                self.add_edge(v, u)
        self.impose_symmetry = update_flag

    def collapse_and_rename(self):
        """Collapses names to ints and indexes 0 .. self.n-1"""
        logging.info("Collapsing graph namespace to 0-indexed set.")
        translation = Translation(*self.edgelist.keys())
        new_edgelist = {}
        for u, neighbors in self.edgelist.items():
            new_edgelist[translation[u]] = [translation[v] for v in neighbors]
        self.edgelist = new_edgelist
        self.translation = translation
        self.translation.lock()

    @staticmethod
    def _get_length_and_log_unit(filename):
        logging_unit = 1
        file_length = 1
        if logging.getLogger('').getEffectiveLevel() <= logging.DEBUG:
            with open(filename) as f:
                logging.debug("Determining file size...")
                t0 = time.time()
                file_length = sum(1 for _ in f)
                t1 = time.time()
                logging_unit = file_length // 100
                logging.debug("Determined file to have {} lines (in {:.3f} seconds)".format(file_length, t1 - t0))
                logging.debug("Intending to be verbose about it every {} lines...".format(logging_unit))
        return file_length, logging_unit

    def load_from_edgelist(self, filename, use_sets_to_improve_runtime=True):
        assert not use_sets_to_improve_runtime or not self.allow_multiedge, "Multi-sets not implemented.  (Would that even save time?)"
        logging.info("Loading graph from edgelist: {!r}".format(filename))
        file_length, logging_unit = self._get_length_and_log_unit(filename)
        big_pile_of_edges = set()
        node_names = set()
        with open(filename) as f:
            i = 0
            for line in f:
                i += 1
                if logging.getLogger('').getEffectiveLevel() <= logging.DEBUG and i % logging_unit == 0:
                    logging.debug("Aggregating edges... On line {} of {} ({:02.1f}%)".format(i, file_length,
                                                                                             i / file_length * 100))
                if not line.strip() or line.strip()[0] in "%#;":
                    continue
                assert len(line.split()) == 2, (
                    "Line %d (%s) is does not contain exactly two nodes."
                    % (i, line.strip()))
                source, target = line.split()
                if not isinstance(source, self.node_type):
                    source = self.node_type(source)
                if not isinstance(target, self.node_type):
                    target = self.node_type(target)
                if not use_sets_to_improve_runtime:
                    self.add_edge(source, target)
                else:
                    big_pile_of_edges.add((source, target))
                    node_names.add(source)
                    node_names.add(target)

        if use_sets_to_improve_runtime:
            logging.debug("Smashing through the edge set...")
            self.edgelist = {u: set() for u in node_names}
            for u, v in big_pile_of_edges:
                self.add_edge(u, v, insert_as='set')
            logging.debug("List-ifying...")
            for u in node_names:
                self.edgelist[u] = sorted(list(self.edgelist[u]))

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
                        self.impose_symmetry,
                        self.allow_multiedge,
                        self.allow_loops))

    def write_edgelist(self, fileout, width=0, spacer=" ", header=""):
        """infer width on width=-1"""
        logging.info("Writing edgelist to file {!r}".format(fileout))
        width = width if width != -1 else max(len(str(k)) for k in self.edgelist)
        buff = ""
        if header:
            buff += "# " + header.strip().lstrip("#") + "\n#\n"
        buff += self.get_properties_header()
        fstr = "{{:{}}}".format(width)
        form = lambda x: fstr.format(x)
        i = 0
        logging.debug("Building buffer...")
        for v in sorted(self.edgelist.keys()):
            i += 1
            if self.n and i % (self.n // 100) == 0:
                logging.debug("On {} of {} ({}%)...".format(i, self.n, i / self.n * 100))
            for n in sorted(self.edgelist[v]):
                buff += spacer.join(map(form, (v, n))) + "\n"
        if fileout is None:
            print(buff)
        else:
            with open(fileout, 'w') as o:
                logging.info("Performing write.")
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


class InvalidEdgeException(Exception):
    pass
