'''Plots the expected gain and loss as a function of elo difference,
assuming by default k=32

'''

import matplotlib.pyplot as plt

def compute_gain(elo_diff, k=32):
    E_a = 1 / (1 + 10 **(elo_diff / 400))
    delta_win  = k * (1 - E_a)
    delta_lose = k * ( - E_a)
    return (delta_win, delta_lose)

def elo_plot():
    x = range(-300, 301, 10)
    wins = [compute_gain(i)[0] for i in x]
    loss = [-compute_gain(i)[1] for i in x]
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, wins, 'g-')
    ax2.plot(x, loss, 'r-')
    ax1.set_xlabel('[Their elo] - [Your elo])')
    ax1.set_ylabel('Potential elo gain', color='g')
    ax2.set_ylabel('Potential elo loss', color='r')
    plt.savefig("elo_delta.png")

