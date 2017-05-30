#!/usr/bin/env python3

"""Framework for Iterated Function Systems"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt

plt.ion()


class IFS:
    WARN_ON_SET_SIZE = 2 ** 16

    def __init__(self, a, b, c, d, seed=1, *additional_seeds):
        self.a, self.b, self.c, self.d = a, b, c, d
        self.points = {seed}
        self.points.update(additional_seeds)
        self.name = "IFS"
        self.iteration = 0
        self.disable_warning = False

    def __repr__(self):
        return "<IFS>"

    def __str__(self):
        return "{} : {}".format(self.name,
                                ", ".join(
                                    str(x)
                                    for x in (self.a, self.b, self.c, self.d)))

    def iterate(self, n_iterations=1, warn=True):
        if warn and not self.disable_warning and len(self.points) >= IFS.WARN_ON_SET_SIZE:
            print("IFS already large: {}".format(self))
            print("Attempting to iterate on IFS with current set size of {}.".format(len(self.points)))
            input("Continue with iteration?  Press ENTER to continue, or KeyboardInterrupt ")
        for _ in range(n_iterations):
            self._perform_single_iteration()

    def _perform_single_iteration(self):
        """Maps z -> {az + bz', c(z-1) + d(z'-1)+1}, where z' denotes the
conjugate of z"""
        self.iteration += 1
        p1 = [self.a * z + self.b * z.conjugate()
              for z in self.points]
        p2 = [self.c * (z - 1) + self.d * (z.conjugate() - 1) + 1
              for z in self.points]
        self.points = p1 + p2

    def plot(self, *args, **kwargs):
        plt.plot([p.real for p in self.points], [p.imag for p in self.points],
                 *args, **kwargs)


def decompose(pts):
    l = list(pts)
    return [p.real for p in l], [p.imag for p in l]


# Recommended calling: plot_sequence(ifs, 15, '.', markersize=1)
def plot_sequence(an_ifs, n, *args, **kwargs):
    for i in range(n):
        plt.clf()
        an_ifs.plot(*args, **kwargs)
        plt.title(str(an_ifs))
        plt.show()
        an_ifs.iterate()
        input("Press ENTER to continue to iteration {}. ".format(i))


if __name__ == "__main__":
    DRAGON_PARAMS = (1 / 2 - 1j / 2, 0, 1 / 2 - 1j / 2, 0,)
    DRAGON = IFS(*DRAGON_PARAMS)
    DRAGON.name = "Dragon"
    DRAGON.disable_warning = True

    DEMO_IFS = DRAGON
    n = 20
    # def animate(ifs, n, *args, **kwargs):
    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
    line, = ax.plot(*decompose(DEMO_IFS.points), '.', markersize=2)


    def init():
        print("in init")
        line.set_data([], [])
        print("exiting init")
        return line,


    def update(_):
        print("in update, ifs.iteration = {}".format(DEMO_IFS.iteration))
        DEMO_IFS.iterate()
        print("update data")
        line.set_data(*decompose(DEMO_IFS.points))
        print("exit update")
        return line,


    ani = animation.FuncAnimation(fig, update, init_func=init,
                                  frames=n, interval=1, repeat=False)
    plt.show()
    input("Press ENTER to exit.")


