from collections import Counter
def new(l):
    # I made this so very, very needlessly complicated...
    my_factors = {}
    count = 0
    for j in range(len(l)):
        factor_count = 0
        for i in range(j):
            if not l[j] % l[i]:
                factor_count += 1
                count += my_factors[i]
        my_factors[j] = factor_count
    return count


def answer(l):
    chain_lengths = [[] for i in range(len(l))]
    for i in range(len(l)):
        for j in range(i):
            if not l[i] % l[j]:
                chain_lengths[i].extend( (x + 1 for x in chain_lengths[j]))
    return chain_lengths
    count = 0
    seen = Counter()
    for i in range(len(i)):
        item = l[i]
        factors = factorize(item)
        seen.update([item])











def test2(l, slow=False):
    primes = sieve_primes(1000)
    masks = [n_to_mask(n, primes) for n in l]
    longest = max(len(m.rstrip('0')) for m in masks)
    masks = [m[:longest] for m in masks]
    pprint(masks)
    return sievsum(masks)

def sievsum(masks):
    count = 0
    are_factors = { i : { j : mask_less(masks[i], masks[j])
                          for j in range(i+1, len(masks))
                      } for i in range(len(masks)) }
    factors_before_here = {j : sum( are_factors[i].get(j) or 0
                                    for i in range(len(masks)) )
                           for j in range(len(masks))}
    # |(i, j, k) | = sum_k( factors_before[j] are_factors[j][k] )
    return sum( factors_before_here[j] * are_factors[j][k] 
                for k in range(len(masks))
                for j in range(k)
            )
    


def mask_less(m1, m2):
    return all(m1[i] <= m2[i] for i in range(len(m1)))

def mask_less3(m1, m2, m3):
    return all(m1[i] <= m2[i] <= m3[i] for i in range(len(m1)))

def slowsum(masks):
    count = 0
    for i in range(len(masks) - 2):
        for j in range(i+1, len(masks) - 1):
            for k in range(j+1, len(masks)):
                if mask_less3(masks[i], masks[j], masks[k]):
                    #print(i, j, k)
                    count += 1
    return count


def fastsum(masks):
    return sum( sum( sum( 1
                          for k in range(j+1, len(masks) )
                          if mask_less(masks[j], masks[k]))
                     for j in range(i+1, len(masks) - 1)
                     if mask_less(masks[i], masks[j]))
                for i in range(0, len(masks) - 2) )
    
def to_base_20(n):
    if n < 10:
        return str(n)
    return "abcdefghij"[n-10]

def fact_to_mask(factors, primes):
    counts = Counter(factors)
    return "1"+"".join([to_base_20(counts[p]) for p in primes])

def n_to_mask(n, primes):
    return fact_to_mask(factorize(n), primes)



def factorize(n):
    primes = sieve_primes(1000)
    factorization = []
    for p in primes:
        while not n % p:
            factorization.append(p)
            n = n // p
        if n == 1:
            break
    return factorization







def check_cache(div, l, i, j, primes=()):
    if l[i] == 1:
        return True
    print("div", i, j, "=", div[i][j])
    if div[i][j] is None:
        if j in primes:
            for x in range(len(l)):
                div[x][j] = False
        else:
            div[i][j] = not (l[j] % l[i])
    print("div", i, j, "=", div[i][j])
    return div[i][j]


def sieve_primes(n):
    sieve = [True] * (n+1)
    sieve[0] = False
    sieve[1] = False
    for i in range(len(sieve)):
        if sieve[i]:
            sieve[2*i:len(sieve):i] = (
                [False] * sum(1 for i in range(2*i, len(sieve), i)))
    return [i for i, b in enumerate(sieve) if b]
    

def factorize(n):
    primes = sieve_primes(1000)
    factorization = []
    for p in primes:
        while not n % p:
            factorization.append(p)
            n = n // p
        if n == 1:
            break
    return factorization
    

# def answer(l):
#     '''Write a function answer(l) that takes a list of positive integers l
#     and counts the number of "lucky triples" of (lst[i], lst[j],
#     lst[k]) where i < j < k.

#     (x, y, z) is lucky if x div y and y div z

#     '''

#     factors = [factorize(n) for n in l]
#     from pprint import pprint
#     pprint(factors)
#     factors_before_pos = {}
#     for i in range(len(l)-1, -1, -1):
#         factors_before_pos[i] = sum(1
#                                     for j in range( i -1, -1, -1)
#                                     if factors[i].issubset(factors[j]))
#     pprint(factors_before_pos)
#     return
#     # max len 2k, max val 1M
#     # Let's just do the prime factorizations of each...
    
#     # Don't do redundant work.
#     # divides[i][j] = True/False if l[i] divides l[j]
#     cache = {i : {j:None for j in range(len(l))}
#              for i in range(len(l))}
#     # nothing divides a prime...
#     primes = sieve_primes(1000000)
#     for i in range(len(cache)):
#         for j in range(i+1, len(cache)):
#             if l[j] in primes:
#                 cache[i][j] = False
#     # except for ones
#     for i in range(len(cache)):
#         for j in range(i+1, len(cache)):
#             if l[j] == 1:
#                 cache[i][j] = True
#     count = 0
#     for i in range(0, len(l) - 2):
#         blah(l[i])
#         for j in range(i + 1, len(l) - 1):
#             blah(l[i], l[j])
#             if not check_cache(cache, l, i, j, primes):
#                 continue
#             for k in range(j + 1, len(l)):
#                 if not check_cache(cache, l, j, k, primes):
#                     blah(l[i], l[j], l[k])
#                     continue
#                 blah(l[i], l[j], l[k], append="<< ++")
#                 count += 1
#     return count
                
    
# def blah(*args, append=""):
#     args = args + ("*",) * (3 - len(args))
#     print("{:>3} {:>3} {:>3}".format(*args) + append)


# def slow_answer(l):
#     print(l)
#     count = 0
#     for i in range(len(l)-2):
#         print("i =", i, l[i])
#         for j in range(i+1, len(l)-1):
#             print("  j =", j, l[j])
#             if not l[j] % l[i]:
#                 for k in range(j+1, len(l)):
#                     print("    k =", k, l[k])
#                     if not l[k] % l[j]:
#                         print("      ++")
#                         count += 1
#     return count

def test():
    print()
    print(answer([1, 1, 1]))
    print()
    print(answer([1, 2, 3, 4, 5, 6]))
