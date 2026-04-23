import math
import numpy as np
import matplotlib.pyplot as plt

def make_figure():
    theta = np.arange(0, 2 * math.pi, 0.01)
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    x = np.cos(theta)
    y = np.sin(theta) * np.cos(theta)   # = 0.5 * sin(2θ)
    axes.plot(x, y)
    axes.set_aspect('equal')
    axes.set_title('Infinity ∞')
    return fig