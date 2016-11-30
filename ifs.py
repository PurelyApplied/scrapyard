#!/usr/bin/env python3

'''Framework for Iterated Function Systems'''
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

    def animate(self, *args, **kwargs):
        fig, ax = plt.subplots()
        ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
                                      interval=25, blit=True)
        pass

    
dragon_params = ( 1/2 - 1j / 2, 0, 1/2 - 1j / 2, 0,)
d = IFS(*dragon_params)
d.name = "Dragon"

# WARNING: be careful about running this repeatedly; it's not
# resetting the IFS, so you might get a large memory demand.

# Recommended calling: plot_sequence(ifs, 15, '.', markersize=1)
def plot_sequence(ifs, n, *args, **kwargs):
    for i in range(n):
        plt.clf()
        ifs.plot(*args, **kwargs)
        plt.title(str(ifs))
        plt.show()
        ifs.iterate()
        input("Press ENTER to continue to iteration {}. ".format(i))






        
# Animation example:
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

fig1 = plt.figure()

data = np.random.rand(2, 25)
l, = plt.plot([], [], 'r-')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('x')
plt.title('test')
line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
                                   interval=50, blit=True)
#line_ani.save('lines.mp4')

fig2 = plt.figure()

x = np.arange(-9, 10)
y = np.arange(-9, 10).reshape(-1, 1)
base = np.hypot(x, y)
ims = []
for add in np.arange(15):
    ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000,
                                   blit=True)
#im_ani.save('im.mp4', metadata={'artist':'Guido'})

plt.show()
