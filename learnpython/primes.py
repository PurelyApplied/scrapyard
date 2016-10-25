'''Beacuse prime generators always come up in /r/learningpython, I have a go-to primes generator examples.'''



def brute_force_is_prime(n):
    '''Test every number from 1 to n as a possible factor for n'''
    # Yes, you could make this slightly better, start at 2, go to
    # sqrt(n), or taking different steps.  But ultimately, your brute
    # force approach is going to be more or less the same, up to a
    # linear factor.
    for factor in range(1, n):
        if n % factor == 0:
            return False
    return True


def from_known(end):
    '''Less brutish force, checking only those numbers that you already
know to be prime.  There's no point checking 4 as a factor, for
instance, if you know 2 wasn't a factor.'''
    
    known = []
    for num in range(2, end):
        # Using 'any' and a generator is good for efficiency.
        if not any(num % factor == 0 for factor in known):
            known.append(num)
    return known


def seive(end):
    '''Build a Sieve of Eratosthenes'''
    # This is pretty much the same as the above, except you start with
    # a larger-than-necessary list and cross-off the ones you don't
    # need, as opposed to starting with a small list and adding the
    # primes that you do need.
    s = [True] * (end+1)
    s[0] = False
    s[1] = False
    for n in range(end + 1):
        if s[n]:
            s[n + n:end+1:n] = [False] * len(s[n + n:end+1:n])
    return [n for n, is_p in enumerate(s) if is_p]


