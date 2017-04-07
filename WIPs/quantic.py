'''An implementation of a terminal-based Quantum Tic-Tac-Toe.'''

class QuantumTicTacToeGame:
    '''Game object.  Contains a QuantumBoard object, turn counters, and
turn history.'''
    def __init__(self):
        self.board = QuantumBoard()
        self.counters = {"x" : 1, "o" : 1}
        self.history = []
        
    def __repr__(self):
        return "<Game object of Quantum Tic-Tac-Toe>"

    def play(self, p1, p2, x_or_o):
        '''Player x_or_o plays a link between positions p1 and p2'''
        assert p1 in range(1, 10) and p2 in range(1, 10) and x_or_o in "xo"
        self.history.append( (p1, p2, x_or_o) )
        self.board[p1].link_to(self.board[p2], x_or_o,
                               self.counters[x_or_o]) 
        self.counters[x_or_o] += 1

    def load_history(self, L):
        '''Load a game history: a list (p1, p2, x_or_o)'''
        while L:
            self.play(*L.pop(0))

    def display(self):
        self.board.display()

    def get_winner(self):
        '''Determines if there is a winner, returning 'x', 'o', or None''' 
        winning_lines = (
            [(i, i+1, i+2) for i in range(1, 10, 3) ]
            + [ (i, i+3, i+6) for i in range(1, 4, 1) ]
            + [(1, 5, 9), (3, 5, 7)])
        for line in winning_lines:
            pass
        return None

    def get_move(self, player, is_AI):
        if not is_AI:
            p1, p2 = self.prompt_for_move()
        else:
            print("AI here!")
            pass
            
        return p1, p2

    def prompt_for_move(self):
        while True:
            try:
                p1 = int(input("Enter position 1:  "))
                p2 = int(input("Enter position 2:  "))
            except ValueError:
                print("Could not convert entered value to int.")
            return p1, p2

    def start_game(self,
                   x_is_AI=False, o_is_AI=False, pause_between_plays=True):
        current_player = 'x'
        is_AI = {'x' : x_is_AI, 'o' : o_is_AI}
        while not self.get_winner():
            self.display()
            if pause_between_plays:
                input("(Press ENTER to continue.) ")
            p1, p2 = self.get_move(current_player, is_AI[current_player])
            self.play(p1, p2, current_player)
            maybe_loops = self.detect_loops(p1, p2)
            if maybe_loops:
                self.resolve_loops(maybe_loops)
            current_player = 'o' if current_player == 'x' else 'x'

    def detect_loops(self, p1, p2):
        inp = input("Enter space-separated loop, if one exists.\n >>  ")
        return [int(i) for i in inp.split()]

    def resolve_loops(self, loop):
        first_link = self.board.get_link(loop[0], loop[1])
        print("Loop identified!")
        print("Collapse {}{} link (positions {}--{}) to which position?".format(
            first_link.owner, first_link.value,
            first_link.tile1.pos, first_link.tile2.pos
        ))
        to = 0
        lookup = {first_link.tile1.pos : first_link.tile1,
                  first_link.tile2.pos : first_link.tile2 }
        while not to:
            try:
                inp = int(input(">> "))
                print(inp, (first_link.tile1.pos, first_link.tile2.pos),
                      inp in (first_link.tile1.pos, first_link.tile2.pos) )
                assert inp in (first_link.tile1.pos, first_link.tile2.pos)
                to = inp
            except ValueError:
                print("Could not interpret input.")
            except AssertionError:
                print("Not one of the given tiles.")
        first_link.collapse(lookup[to])

class QuantumBoard:
    def __init__(self):
        self.container = {i : QuantumTile(i) for i in range(1, 10)}

    def __getitem__(self, pos):
        return self.container[pos]

    def __repr__(self):
        return "<A Quantum Tic-Tac-Toe board>"
        
    def get_link(self, p1, p2):
        return self[p1].links.get(p2, None)
        
        
    def display(self):
        # # Do a full sub-board for each tile.  Max 2 char per sub-tile
        # # 11 12 13 | 21 22 23 | 31 32 33
        # # 14 15 16 | 24 25 26 | 34 35 36
        # # 17 18 19 | 27 28 29 | 37 38 39
        # # ---------+----------+---------
        # # 41 42 43 | 51 52 53 | 61 62 63
        # # 44 45 46 | 54 55 56 | 64 65 66
        # # 47 48 49 | 57 58 59 | 67 68 69
        # # ---------+----------+---------
        # # ...
        
        tile_displays = {i : self.container[i].display_contents()
                         for i in range(1, 10)}
        entries = ["__"] * 81
        i = 0
        for tile, sub in _display_generator():
            entries[i] = tile_displays[tile][sub]
            i += 1
        print(
            "\n{}\n".format("-" * 30).join(
                "\n".join(
                    " | ".join(
                        " ".join(
                            entries[start : start + 3]
                        ) for start in range(row_start, row_start + 9, 3)
                    ) for row_start in range(tile_start, tile_start + 27, 9)
                ) for tile_start in range(0, 81, 27)
            )
        )
        
class QuantumTile:
    def __init__(self, position):
        self.pos = position
        self.links = {}
        self.resolved = False
        self.resolved_owner = None
        self.resolved_value = None

    def __repr__(self):
        return "<A Quantum Tic-Tac-Toe tile (position {})>".format(self.pos)

    def link_to(self, other, owner, value):
        link = QuantumLink(self, other, owner, value) 
        self.links[other.pos] = link
        other.links[self.pos] = link

    def display_contents(self):
        if not self.resolved:
            return { i : self.links.get(i, None).tiny_str()
                     if self.links.get(i, None)
                     else "__"
                     for i in range(1, 10) }
        r = { i : "  " for i in range(1, 10) }
        if self.resolved_owner == "x":
            r.update({ 2: "\\/",
                       5: "/\\",
                       9: " {}".format(self.resolved_value)})
        else:
            r.update({ 2: "/\\",
                       5: "\\/",
                       9: " {}".format(self.resolved_value)})
        return r

    def resolve(self, owner, value):
        self.resolved = True
        self.resolved_owner = owner
        self.resolved_value = value
        for l in self.links.values():
            if not l.collapsed:
                tile_to_collapse = l.tile1 if not l.tile1 is self else l.tile2
                l.collapse(tile_to_collapse)

class QuantumLink:
    def __init__(self, tile1, tile2, owner, value):
        self.tile1 = tile1
        self.tile2 = tile2
        self.owner = owner
        self.value = value
        self.collapsed = False

    def __repr__(self):
        return "<{}-{} link between {} and {}>".format(
            self.owner, self.value, self.tile1, self.tile2)

    def touches(self, pos):
        return pos in (self.tile1.pos, self.tile2.pos)

    def tiny_str(self):
        return "{}{}".format(self.owner, self.value)

    def collapse(self, tile):
        assert tile in (self.tile1, self.tile2)
        self.collapsed = True
        tile.resolve(self.owner, self.value)

def _display_generator():
    for i in range(81):
        row = i // 9
        col = i % 9
        meta_row = row // 3
        meta_col = col // 3
        tile = meta_col + 3 * meta_row
        sub = col % 3 + 3 * (row % 3)
        # Remember that these should be 1-indexed since they are used
        # player-side
        yield tile + 1, sub + 1
       
        
_text_colors = {
    'HEADER' : '\033[95m',
    'OKBLUE' : '\033[94m',
    'OKGREEN' : '\033[92m',
    'WARNING' : '\033[93m',
    'FAIL' : '\033[91m',
    'ENDC' : '\033[0m',
    'BOLD' : '\033[1m',
    'UNDERLINE' : '\033[4m'
}

def color_print(text, color):
    if not _text_colors.get(color, None):
        print(text)
    else:
        print("{}{}{}".format(_text_colors[color],
                              text,
                              _text_colors["ENDC"]))


print('done.')

def play_quant(game = None):
    if not game:
        game = QuantumTicTacToeGame()
    game.start_game(pause_between_plays=False)

def test_quant():
    G = QuantumTicTacToeGame()
    P = [ (1, 2, 'x'),
          (2, 3, 'o'),
          (3, 5, 'x'),
          (1, 9, 'o') ]
    G.load_history(P)
    return G

def test():
    play_quant(test_quant())
