""" Homegrown prime-related functions. """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

import itertools
try:
    from math import sqrt, isqrt
except ImportError:
    # Python < 3.8
    isqrt = lambda n: int(sqrt(n))


#######################################################################################################################
#
#   is_prime_baseline
#
#######################################################################################################################

def is_prime_baseline(n):
    """ Dead simple function to validate and baseline prime-related code. """
    if n == 1: return False
    if n == 2: return True
    elif n % 2 == 0: return False
    for m in range(3, isqrt(n) + 1, 2):
        if n % m == 0: return False
    return True


#######################################################################################################################
#
#   is_prime
#
#######################################################################################################################

def is_prime(n):
    # Anything less than 1 is not prime
    if n < 2: return False
    # Anything less then 4 is prime.
    elif n < 4: return True
    # Even numbers >= 4 are not prime.
    elif n % 2 == 0: return False
    # Numbers divisible by an existing prime up to their sqrt are not prime.
    limit = isqrt(n)
    for p in is_prime.primes:
        if p > limit: break
        elif n % p == 0: return False
    # Numbers with a factor between the last cached prime and the sqrt of the number are not prime.
    for m in range(is_prime.primes[-1] + 2, limit + 1, 2):
        # (Cache any new primes we find while looking for factors)
        if not any(p for p in is_prime.primes if m % p == 0): is_prime.primes.append(m)
        if n % m == 0: return False
    return True

is_prime.primes = [2, 3]


#######################################################################################################################
#
#   erat3
#
#######################################################################################################################

def erat3( ):
    """ Efficient prime generator. Source: https://stackoverflow.com/a/3796442 """
    D = { 9: 3, 25: 5 }
    yield 2
    yield 3
    yield 5
    MASK= 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS= frozenset( (1, 7, 11, 13, 17, 19, 23, 29) )

    for q in itertools.compress(
            itertools.islice(itertools.count(7), 0, None, 2),
            itertools.cycle(MASK)):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D or (x%30) not in MODULOS:
                x += 2*p
            D[x] = p


#######################################################################################################################
#
#   primes
#
#######################################################################################################################

def primes(n):
    return tuple(itertools.takewhile(lambda p: p < n, erat3()))


#######################################################################################################################
#
#   AsYouGoCachingIterable
#
#######################################################################################################################

class AsYouGoCachingIterable:
    """ Caching iterable from generator. Source: https://stackoverflow.com/a/19504173 """
    def __init__(self, iterable):
        self.iterable = iterable
        self.iter = iter(iterable)
        self.done = False
        self.vals = []

    def __iter__(self):
        if self.done:
            return iter(self.vals)
        return itertools.chain(self.vals, self._gen_iter())

    def _gen_iter(self):
        for new_val in self.iter:
            self.vals.append(new_val)
            yield new_val
        self.done = True


#######################################################################################################################
#
#   PrimesIterator
#
#######################################################################################################################

class PrimesIterator(AsYouGoCachingIterable):
    def __init__(self):
        super().__init__(iterable=erat3())

    def primes(self, n):
        for p in itertools.takewhile(lambda p: p <= n, self):
            yield p


#######################################################################################################################
#
#   primes_experimental
#
#######################################################################################################################

def primes_experimental(n):
    for p in itertools.takewhile(lambda p: p <= n, primes_experimental.primes_iterator):
        yield p
primes_experimental.primes_iterator = PrimesIterator()


#######################################################################################################################
#
#   is_prime_experimental
#
#######################################################################################################################

def is_prime_experimental(n):
    # Anything less than 1 is not prime
    if n < 2:
        return False
    # Anything less then 4 is prime.
    elif n < 4:
        return True
    # Numbers divisible by an existing prime up their sqrt are not prime.
    for p in primes_experimental(isqrt(n)):
        if n % p == 0: return False
    # It's prime.
    return True


#######################################################################################################################
#
#   check_equivalence
#
#######################################################################################################################

def check_equivalence(fns, values):
    for value in values:
        if len(set(fn(value) for fn in fns)) != 1:
            msg = f"{value}\n" + "".join(f"{fn.__name__}({value}): {fn(value)}\n" for fn in fns)
            raise ValueError(msg)


#######################################################################################################################
#
#   check_performance
#
#######################################################################################################################

def check_performance(fns, values, repetitions=1):
    from time import process_time as timer
    for fn in fns:
        start = timer()
        for n in range(repetitions):
            for value in values:
                fn(value)
        print(f"{fn.__name__}: {timer() - start}")


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################


if __name__ == "__main__":
    fns = [is_prime, is_prime_baseline, is_prime_experimental]
    check_equivalence(fns, range(1, 100))
    check_performance(fns, range(1, 5000000), 1)
