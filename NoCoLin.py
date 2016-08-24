'''Brute force search for the following problem: given an N x N
coordinate grid, choose N points such that no two points share a
horizontal, vertical, or diagonal line.

This problem stumped my girlfriend and I in its 8x8 incarnation at
OMSI.  This implementation is recursive, and not efficiently so.  Not
recommended for problems of size N>10.

'''
import random

def main(n, verbose=False):
    sol = recursive_step([], n, verbose)
    if sol:
        plot = [ ["_" for x in range(n)] for y in range(n) ]
        for point in sol:
            plot[point[0]][point[1]] = "x"
        for line in plot:
            print(" ".join(line))
    else:
        print("No solution found.")

#%%
def recursive_step(sol, n, verbose=False):
    if len(sol) == n:
        if verbose:
            print("Evaluating solution:", sol)
        if evaluate(sol, verbose):
            return sol
        else:
            return []

    X_sol = [i[0] for i in sol]
    Y_sol = [i[1] for i in sol]
    X_rem = [i for i in range(n) if not i in X_sol]
    Y_rem = [i for i in range(n) if not i in Y_sol]
    Pool = [(x,y) for x in X_rem for y in Y_rem]
    random.shuffle(Pool)
    if verbose:
        print("Point pool:", Pool)
    for point in Pool:
        ret = recursive_step(sol + [point], n, verbose)
        if ret:
            return ret
    return []

#%%        
def evaluate(sol, verbose=False):
    Xs = [i[0] for i in sol]
    for x in Xs:
        if Xs.count(x) > 1:
            if verbose:
                print("Vertical line detected.")
            return False
    Ys = [i[1] for i in sol]
    for y in Ys:
        if Ys.count(y) > 1:
            if verbose:
                print("Horizontal line detected.")
            return False
    # / diagonal: x - y is unique
    # \ diagonal: x + y is unique
    slash_key_val = [i[0] - i[1] for i in sol]
    for key in slash_key_val:
        if slash_key_val.count(key) > 1:
            if verbose:
                print("Foreslash detected.")
            return False
    backslash_key_val = [i[0] + i[1] for i in sol]
    for key in backslash_key_val:
        if backslash_key_val.count(key) > 1:
            if verbose:
                print("Backslash detected.")
            return False
    
    if verbose:
        print("No line conflicts detected.")
    return True
