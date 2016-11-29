#!/usr/bin/env python3

'''Framework for Iterated Function Systems'''
import cmath
from numbers import Complex
import matplotlib.pyplot as plt
plt.ion()


class IFS:
    def __init__(self, a, b, c, d, seed=1, *additional_seeds):
        self.a, self.b, self.c, self.d = a, b, c, d
        self.points = [seed]
        self.points.extend(additional_seeds)
        self.name = "IFS"
        
    def __repr__(self):
        return "<IFS>"

    def __str__(self):
        return "{} ({})".format(self.name,
            ", ".join(
                str(x)
                for x in (self.a, self.b, self.c, self.d)))
    
    def iterate(self, n=1):
        #TODO: warn on large iterations / large current self.points.
        #Exponential memory growth
        for _ in range(n):
            self._perform_single_iteration()

    def _perform_single_iteration(self):
        '''Maps z -> {az + bz', c(z-1) + d(z'-1)+1}, where z' denotes the
conjugate of z'''
        p1 = [self.a * z + self.b * z.conjugate()
            for z in self.points]
        p2 = [self.c * (z-1) + self.d * (z.conjugate()-1) +1
            for z in self.points]
        self.points = p1+p2
        
    def plot(self, *args, **kwargs):
        plt.plot([p.real for p in self.points], [p.imag for p in self.points],
                 *args, **kwargs)

dragon_params = ( 1/2 - 1j / 2, 0, 1/2 - 1j / 2, 0,)
d = IFS(*dragon_params)
d.name = "Dragon"

def plot_sequence(ifs, n, *args, **kwargs):
    for i in range(n):
        plt.clf()
        ifs.plot(*args, **kwargs)
        plt.title(str(ifs))
        plt.show()
        ifs.iterate()
        input("Press ENTER to continue to iteration {}. ".format(i))
        
