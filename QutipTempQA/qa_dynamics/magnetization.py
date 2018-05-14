import numpy as np
import matplotlib.pyplot as plt
from qutip import *

from .dynamics import *
from QutipTempQA.utils.utils import plot_setting
from QutipTempQA.utils.utils import filename_from

def draw_magnetization(save_path, N, T, system, params):
    sys = system(T, N, params)
    results = dynamics_result(sys, N, T, params)
    tlist, mlist = draw_operator(results,sys.mz(),T)

    plot_setting()
    plt.xlabel('t')
    plt.ylabel('magnetization')
    plt.plot(tlist, mlist)

    figure_path = save_path + filename_from(N, T, params) + '.pdf'
    plt.savefig(figure_path)


def draw_operator(results,operator, T, dt=0.01):
    tlist = np.arange(0,T+dt,dt)
    mlist = [expect(operator, psi) for psi in results]

    return tlist, mlist

