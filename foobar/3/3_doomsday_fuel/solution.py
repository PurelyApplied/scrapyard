from fractions import Fraction
def answer(m):
    '''Returns probability of ending in terminal state with the list 
    [n_1, n_2, n_3, ..., n_k, denom]
    where p_i = n_i / denom
    '''
    if len(m) <= 2:
        return [1, 1]
    # While m is not yet in the correct form, this is an example of an
    # absorbing Markov chain.
    # Step 1: Reform as Markov chain, convertine values to Fraction
    # Step 2: Solve absorbing rates.
    # Ultimately, this is done by setting the chain to the cannonical form
    # P = [ Q  R ]
    #     [ 0  I ]
    # from which it follows...
    # N = (I - Q)^{-1}
    # B = N R
    # where B[i][j] denotes the probability starting in state i
    # ultimately ends in state j

    # Step 1: Reform as absorbing Markov
    # First, any terminal states are currently [0, 0, ... ]
    # We "loop" these states, so that state i -> state i
    stationary = []
    frac_mat = [None] * len(m)
    for i in range(len(m)):
        rowsum = sum(m[i])
        frac_mat[i] = [Fraction(v, rowsum)
                       if rowsum else Fraction(0)
                       for v in m[i]]
        if not rowsum:
            frac_mat[i][i] = Fraction(1)
            stationary.append(i)
    Q, R = get_qr(frac_mat, stationary)
    # N^{-1} = I - Q
    N = inverse([[ (-Q[i][j] + int(i == j))
                   for j in range(len(Q))]
                 for i in range(len(Q))])
    # We will only care about B[0], since we start in state 0
    B = matrix_mult([N[0]], R)
    # Lastly, get the lcm for the denominators.
    denom = lcm(*[v.denominator for v in B[0]])
    return [(v * denom).numerator for v in B[0]] + [denom]


def get_qr(m, stationary):
    '''Returns Q, R of the cannonical form for absorbing Markov chain
    P = [ Q  R ]
        [ 0  I ]
    not to be confused with QR factorization.'''
    Q = []
    R = []
    for i in range(len(m)):
        if i not in stationary:
            Q.append([m[i][j] for j in range(len(m)) if j not in stationary])
            R.append([m[i][j] for j in range(len(m)) if j in stationary])
    return Q, R


def matrix_mult(L, R):
    assert len(L[0]) == len(R), "Inner dimension mismatch in matrix mult."
    # X[i][j] = sum(L[i][:] * R[:][j])
    return [[sum(L[i][k] * R[k][j]
                 for k in range(len(R)))
             for j in range(len(R[0]))]
            for i in range(len(L))]


def inverse(m):
    '''Compute the matrix inverse using Gaussian elimination'''
    # This function could be improved using numpy/scipy/sympy, but
    # they are not part of the stdlib.  I could write something using
    # pivots from scratch, but in practice I wouldn't reinvent the
    # wheel and would use existing code.  Still, I feel that is not in
    # the spirit of this challenge.  This is less efficient, but for a
    # matrix of max size 10, it will do.
    M = [m[i][:] + [Fraction(i == j) for j in range(len(m))]
         for i in range(len(m))]
    # Press down...
    for i in range(len(M)):
        # Position nontrivial row
        if M[i][i] == 0:
            for j in range(i+1, len(M)):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
        # Normalize
        M[i] = [v / M[i][i] for v in M[i]]
        # Reduce below
        for j in range(i+1, len(M)):
            if M[j][i] != 0:
                M[j] = [ M[j][k] - M[i][k] * M[j][i] for k in range(len(M[i]))]
    # And back up
    for i in range(len(M)-1, -1, -1):
        # leading 1 guaranteed now.
        for j in range(i):
            if M[j][i] != 0:
                M[j] = [ M[j][k] - M[i][k] * M[j][i] for k in range(len(M[i]))]
    Minv = [row[len(M):] for row in M]
    return Minv


def gcd(a, b):
    '''Euclid's algorithm for greatest common divisors'''
    if b == 0:
       return a
    else:
       return gcd(b, a % b)


def lcm(a, b, *args):
    '''Returns least common multiple of values provided.'''
    if not args:
        return a * b // gcd(a, b)
    cm = lcm(a, b)
    return lcm(cm, *args)




def show(m, title=""):
    if title:
        print(title)
    print(
        "\n".join(
            " ".join(
                "{:>5}".format(str(v))
                for v in row)
            for row in m))




def test1():
    return [
        [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
        [0,0,0,0,0,0],  # s3 is terminal
        [0,0,0,0,0,0],  # s4 is terminal
        [0,0,0,0,0,0],  # s5 is terminal
    ]

def test3():
    return [
        [0,8,0,0,0,8],  # s0, the initial state, goes to s1 and s5 with equal probability
        [32,0,0,24,16,0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
        [0,0,0,0,0,0],  # s3 is terminal
        [0,0,0,0,0,0],  # s4 is terminal
        [0,0,0,0,0,0],  # s5 is terminal
    ]

def test2():
    return [
        [0,1,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0,0,0,0,0],  # s3 is terminal
        [0,0,0,0,0],  # s4 is terminal
        [0,0,0,0,0],  # s5 is terminal
    ]

    # Given a Markov process with possible cycles, determine the end states.

def test():
    return answer(test1())


from pprint import pprint
