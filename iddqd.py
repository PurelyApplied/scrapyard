#!/usr/bin/env python3
from random import randint, choice
from pprint import pprint
# Reddit's /r/dailyprogrammer challenge #267, available at
# https://www.reddit.com/r/dailyprogrammer/comments/4k8m02/20160520_challenge_267_hard_iddqd/

# Use these as draw and testing constants.  Probably shouldn't be
# using globals.  I'm a bad man.
_target = "X"
_obstacle = "O"
_beam = "@"
_empty = "."

def main(grid=None, rand_graph_args = (10, 10, 10, 10)) -> "grid, best_start":
    if not grid:
        grid = make_random_test(*rand_graph_args)
    firing_options = get_options(grid)
    best_start = None
    best_score = -1
    last_best_score = -2
    while firing_options:
        try:
            if last_best_score < best_score and 0 < best_score:
                print("Current best from {} along {} hits {}".format(
                    best_start[0] if best_start else "NULL",
                    best_start[1] if best_start else "NULL",
                    best_score))
                last_best_score = best_score
            (x, y), (dx, dy) = choice(list(firing_options))
            # print("Starting at ({}, {}), aiming along ({}, {})".format(x, y, dx, dy))
            x, y, dx, dy = get_starting_pos(grid, x, y, dx, dy)
            # print("Adjusted to start at ({}, {}), aiming along ({}, {})".format(x, y, dx, dy))
            score = fire(grid, x, y, dx, dy)
            # print("Hits {} targets!".format(score))
            if score > best_score:
                best_score = score
                best_start = ( (x,y), (dx, dy) )
                # print("A new best!")
            while in_bounds(grid, x, y) and grid[y][x] == _empty:
                firing_options.remove( ((x,y), (dx,dy)) )
                x += dx
                y += dy
        except KeyboardInterrupt:
            print("\n{} potential firing options remain...".format(
                len(firing_options)))
            try:
                input("Interrupt with C-c C-c again to quit, or press ENTER to continue. ")
            except KeyboardInterrupt:
                print("Quitting!")
                break
    return grid, best_start

# Recursive scoring: Look at who you'd hit,
# call fire(grid, x+dx, y+dy, dx, dy)
# If diagonal, divide score by two to avoid double counting.
def fire(grid, x, y, dx, dy):
    score = score_this_pos(grid, x, y, dx, dy)
    if in_bounds(grid, x+dx, y+dy):
        if grid[y+dy][x+dx] == _empty:
            score += fire(grid, x+dx, y+dy, dx, dy)
        elif grid[y+dy][x+dx] == _target:
            score += 1
    return score

# To avoid overlap, a horizontal beam only looks up/down, and a
# diagonal beam only looks "angled forward"
def score_this_pos(grid, x, y, dx, dy):
    score = 0
    if dx and dy:
        if in_bounds(grid, x, y+dy) and grid[y+dy][x] == _target:
            score += 1
        if in_bounds(grid, x+dx, y) and grid[y][x+dx] == _target:
            score += 1
    else:
        # Check +1/-1 for whichever coord is 0
        ty1 = y + (1 if not dy else 0)
        tx1 = x + (1 if not dx else 0)
        ty2 = y - (1 if not dy else 0)
        tx2 = x - (1 if not dx else 0)
        if in_bounds(grid, tx1, ty1) and grid[ty1][tx1] == _target:
            score += 1
        if in_bounds(grid, tx2, ty2) and grid[ty2][tx2] == _target:
            score += 1
    return score
        
# Create a $hei x $wid grid, randomly placing $n_targ targets and
# $n_obst obstacles.  Is not efficient: random-and-redraw approach.
def make_random_test(hei, wid, n_targ, n_obst):
    grid = [ [_empty] * wid for x in range(hei) ]
    while 0 < n_targ:
        x, y = randint(0, wid - 1), randint(0, hei - 1)
        if grid[y][x] == _empty:
            grid[y][x] = _target
            n_targ -= 1
    while n_obst > 0:
        x, y = randint(0, wid - 1), randint(0, hei - 1)
        if grid[y][x] == _empty:
            grid[y][x] = _obstacle
            n_obst -= 1
    return grid

# Print the grid
def print_grid(g, beam=None, col_spacer="", row_spacer="\n"):
    if not beam:
        print(row_spacer.join( col_spacer.join(row) for row in g ))
        return
    grid_copy = [x[:] for x in g]
    (x,y), (dx, dy) = beam
    while in_bounds(g, x, y) and g[y][x] == _empty:
        grid_copy[y][x] = _beam
        x += dx
        y += dy
    print_grid(grid_copy, None, col_spacer, row_spacer)

def in_bounds(g, x, y):
    hei, wid = len(g), len(g[0])
    return 0 <= x < wid and 0 <= y < hei

# Identify all possible blast starts
def get_options(grid):
    opts = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == _empty:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if not (dx == 0 and dy == 0):
                            opts.add( ((x, y), (dx, dy)) )
    return opts


# Given a location and aim, first "back up" if the space is available.
# Fire, tally, report ( (x,y), (dx, dy), n_hit, beam_length)
def get_starting_pos(grid, x, y, dx, dy):
    assert grid[y][x] == _empty, "try_blast called on non-empty space ({}, {})".format(x, y)
    # Back up
    while in_bounds(grid, x-dx, y-dy) and grid[y-dy][x-dx] == _empty:
        x -= dx
        y -= dy
    return x, y, dx, dy
