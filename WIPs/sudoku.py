class Sudoku:
    def __init__(self, n_sub_rows=3, n_sub_cols=3, *args):
        self.size = n_sub_rows * n_sub_cols
        self.card = args if args else [ [0] * self.size
                                        for i in range(self.size) ]
        self.n_sub_cols = n_sub_cols
        self.n_sub_rows = n_sub_rows
        self.pool = set(range(1, self.size + 1))
        self.permissions = {
            (i, j) : self.pool.copy()
            for i in range(self.size)
            for j in range(self.size)
        }
        for row in range(self.size):
            for col in range(self.size):
                if self.card[row][col] > 0:
                    self.set(row, col, self.card[row][col])
        
    def __repr__(self):
        return "<Sudoku: {} square with {} x {} sub>".format(
            self.size, self.n_sub_rows, self.n_sub_cols)

    def get_display(self, col_delim=" ", row_delim="\n",
                    blank=".", box_separater=False):
        ret_str = ""
        for row_num in range(len(self.card)):
            if box_separater and row_num and not row_num % self.n_sub_rows:
                # Hack job
                ret_str += "-" * 20 + "\n"
            row = self.card[row_num]
            for col_num in range(len(row)):
                if box_separater and col_num and not col_num % self.n_sub_cols:
                    ret_str += "{0}|{0}".format(col_delim)
                val = self.card[row_num][col_num]
                if col_num:
                    ret_str += col_delim
                ret_str += str(val) if not val == 0 else blank
            ret_str += row_delim
        return ret_str

    def is_solved(self):
        return not 0 in set(v for r in self.card for v in r)

    def set(self, row, col, val):
        print("Setting position ({}, {}) to {}".format(row, col, val))
        self.card[row][col] = val
        self.permissions[(row, col)] = set()
        self.prune_shared_lines(row, col)
        self.prune_shared_squares(row, col)

    def set_obvious(self):
        do = True
        did_any = False
        while do:
            to_set = list(
                filter(lambda x: len(x[1]) == 1, self.permissions.items()) )
            do = True if to_set else False
            if do and not did_any:
                did_any = True
            for pos, val in to_set:
                self.set(pos[0], pos[1], val.pop())
        return did_any

    def prune_shared_lines(self, row, col):
        val = self.card[row][col]
        for r in range(self.size):
            self.permissions[(r, col)].discard(val)
        for c in range(self.size):
            self.permissions[(row, c)].discard(val)

    def prune_shared_squares(self, row, col):
        val = self.card[row][col]
        start_row = row // self.n_sub_cols * self.n_sub_rows
        start_col = col // self.n_sub_rows * self.n_sub_cols
        for i in range(start_row, start_row + self.n_sub_rows):
            for j in range(start_col, start_col + self.n_sub_cols):
                self.permissions[(i, j)].discard(val)
                

    def cast_lines(self):
        pass


def solve(sudoku):
    attempt = 0
    while not sudoku.is_solved():
        attempt += 1
        did_any = sudoku.set_obvious()
        
        if not did_any:
            raise RuntimeError("Didn't do anything!")
        
    print("Solved in {} passes!".format(attempt))
    


def show(S):
    print(S.get_display(blank='.', box_separater=True))


def test1():
    return Sudoku(2, 2,
                  [1, 3, 2, 4],
                  [2, 4, 1, 0],
                  [4, 1, 0, 0],
                  [3, 2, 0, 0])
    
