import matplotlib.pyplot as plt
import numpy as np

from lib_vars import *
from lib_elements import *
from lib_commands import *
from lib_expressions import *

from construction import *

#--------------------------------------------------------------------------

def Show(constr):
    figure, axes = plt.subplots()
    axes.set_aspect(1)
    axes.set(xlim=(-10, 20), ylim = (-10, 20))

    # оси координат
    plt.axvline(x=0, c="black", alpha=0.1)
    plt.axhline(y=0, c="black", alpha=0.1)

    # отрисовка элементов
    for el in constr.elements:
        if type(el.data) == Point:
            plt.scatter(el.data.a[0], el.data.a[1])
            plt.text(el.data.a[0], el.data.a[1], el.name) #, bbox = dict(facecolor="white",alpha=0.5))

        elif type(el.data) == Line:
            if el.data.n[1] is not 0:
                k = -el.data.n[0] / el.data.n[1]
                b = el.data.c / el.data.n[1]
                x = np.linspace(-20, 20, 100)
                y = k * x + b
            else:
                k = -el.data.n[1] / el.data.n[0]
                b = el.data.c / el.data.n[0]
                y = np.linspace(-20, 20, 100)
                x = k * y + b
            plt.plot(x, y)

        elif type(el.data) == Circle:
            axes.add_artist(plt.Circle((el.data.c[0], el.data.c[1]), el.data.r, fill = False))


    plt.show()