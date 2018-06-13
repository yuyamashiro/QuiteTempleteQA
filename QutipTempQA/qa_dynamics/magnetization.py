import os
import numpy as np
import matplotlib.pyplot as plt
from qutip import *

from .dynamics import *
from QutipTempQA.utils.utils import plot_setting
from QutipTempQA.utils.utils import filename_from

def draw_magnetization(save_path, N, T, system, params, variables):

    plot_setting(font_size=10)
    plt.xlabel('t',fontsize=12)
    plt.ylabel('magnetization',fontsize=12)

    for var in variables[1]:
        params[variables[0]] = var

        data_path = './data/m_vs_t/mag_' + filename_from(N, T, params, system.params_name) + '.dat'
        if os.path.exists(data_path):
            print('load data of time evolution of magnetization')
            tlist ,mlist = np.loadtxt(data_path)
        else:
            print('**** calculate data of time evolution of magnetization ****')
            sys = system(T, N, params)
            results = dynamics_result(sys, N, T, params, only_final=False).states
            tlist, mlist = calc_operator(results, sys.mz(), T)
            np.savetxt(data_path, [tlist, mlist])

        plt.plot(tlist, mlist,label=variables[0] + '=' + str(var))

    figure_path = save_path + filename_from(N, T, params, system.params_name) + '.pdf'
    plt.legend()
    plt.savefig(figure_path, bbox_inches="tight", pad_inches=0.1)


def calc_operator(results,operator, T, dt=0.01):
    tlist = np.arange(0,T+dt,dt)
    mlist = [expect(operator, psi) for psi in results]

    return tlist, mlist


def draw_dist_magnetization(save_path, N, T, system, params, bar_width=0.3):
    plt.figure()
    plot_setting(font_size=10)
    plt.xlabel('magnetization',fontsize=12)
    plt.ylabel('probability',fontsize=12)

    data_path = './data/m_dist/m_dist_' + filename_from(N, T, params, system.params_name) + '.dat'
    if os.path.exists(data_path):
        print("load data of distribution of magnetization at final state")
        mlist, prob_list = np.loadtxt(data_path)
    else:
        print("calculate distribution of magnetization at final state")
        sys = system(T, N, params)
        mz,m_basis = sys.mz().eigenstates()
        results = dynamics_result(sys, N, T, params)
        probs = [np.abs((mb.dag() * results).full()[0][0]) ** 2 for mb in m_basis]

        u_mz_prob = dict([[m,0] for m in np.unique(mz)])
        for mag, p in zip(mz, probs):
            u_mz_prob[mag] += p

        mlist = list(u_mz_prob.keys())
        prob_list = list(u_mz_prob.values())
        np.savetxt(data_path, [mlist, prob_list])

    plt.xticks(mlist)
    plt.bar(mlist, prob_list, width=bar_width,align="center")

    figure_path = save_path + filename_from(N, T, params, system.params_name) + '.pdf'
    plt.savefig(figure_path, bbox_inches="tight", pad_inches=0.0)
