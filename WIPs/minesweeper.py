'''A minesweeper solver, as presented in https://www.reddit.com/r/dailyprogrammer/comments/50s3ax/20160902_challenge_281_hard_minesweeper_solver/'''

def test():
    MS = Minesweeper()
    MS.add_mines((0, 1), (2, 0))
    MS.reveal((1, 1))
    MS.reveal((0, 1))
    MS.reveal((0, 0))
    print(MS.draw())

class Tile:
    def __init__(self, pos, has_mine=False):
        self.x, self.y = pos
        self.has_mine = has_mine
        self.known = False

    def __repr__(self):
        return "<Tile>"


    def as_char(self, ms):
        if not self.known:
            return "?"
        elif self.has_mine:
            return "X"
        else:
            neighbors = [(self.x + i, self.y + j)
                         for i in (-1, 0, 1)
                         for j in (-1, 0, 1)
                         if not i == j == 0
                         and 0 <= self.x + i < ms.x
                         and 0 <= self.y + j < ms.y]
            #print(list(neighbors))
            count = 0
            for n in neighbors:
                #print(n)
                #print(ms.board[n].has_mine)
                if ms.board[n].has_mine:
                    count += 1
            if count == 0:
                for n in neighbors:
                    print(n)
                    ms.reveal(n)

            return str(count) if count else " "


class Minesweeper:
    def __init__(self, size=(10,10), mines=()):
        self.x, self.y = size
        self.board = {(i, j) : Tile((i, j))
                      for i in range(size[0])
                      for j in range(size[1])}
        for m in mines:
            self.board[m].has_mine = True
    
    def __repr__(self):
        return "<Minesweeper>"

    def add_mines(self, *args):
        for pos in args:
            self.board[pos].has_mine = True

    def reveal(self, pos):
        self.board[pos].known = True
        
    def reveal_all(self):
        for t in self.board.values():
            t.known = True

    def draw(self):
        return "\n".join(
            "".join(
                self.board[(i, j)].as_char(self) for i in range(self.x)
            ) for j in range(self.y))


