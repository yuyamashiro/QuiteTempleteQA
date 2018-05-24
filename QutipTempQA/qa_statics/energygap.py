import os

import numpy as np
import matplotlib.pyplot as plt

from QutipTempQA.utils.utils import plot_setting
from QutipTempQA.utils.utils import filename_from

def draw_energygap(fig_path, N, system, params, variables):

    plt.figure()
    plot_setting()
    tlist = np.arange(0,1.01,0.01)
    for var in variables[1]:
        params[variables[0]] = var

        data_path = "./data/spectrum/spect_" + filename_from(N, '_', params, names=system.params_name) + ".dat"

        if os.path.exists(data_path):
            print("-- {} is exist -- will load".format(data_path))
            spectrum = np.loadtxt(data_path)
        else:
            print("*** {} is not exist *** calculating ...".format(data_path))
            sys = system(T=1,N=N,param=params)
            #gap = []
            spectrum = []
            for t in tlist:
                spectrum.append(sys.H(t).eigenstates()[0])
                #gap.append(spectrum[1] - spectrum[0])
            np.savetxt(data_path, spectrum)

        gap = []
        for energy in spectrum:
            gap.append(energy[1] - energy[0])

        plt.plot(tlist, gap, label=variables[0] + '=' + str(var))
    plt.legend()
    plt.xlabel('s', fontsize=12)
    plt.ylabel('energy gap', fontsize=12)
    plt.savefig(fig_path+'gap' + filename_from(N,1,params,system.params_name) + '.pdf')


def draw_min_gap(fig_path, Nlist, system, params, variables):
    plt.figure()
    plot_setting(font_size=10)
    tlist = np.arange(0, 1.01, 0.01)

    for var in variables[1]:
        params[variables[0]] = var
        min_gap = []

        for N in Nlist:

            data_path = "./data/spectrum/spect_" + filename_from(N, '_', params, names=system.params_name) + ".dat"

            if os.path.exists(data_path):
                print("-- {} is exist -- will load".format(data_path))
                spectrum = np.loadtxt(data_path)
            else:
                print("*** {} is not exist *** calculating ...".format(data_path))
                sys = system(T=1, N=N, param=params)
                spectrum = []
                for t in tlist:
                    spectrum.append(sys.H(t).eigenstates()[0])
                np.savetxt(data_path, spectrum)

            gap = []
            for energy in spectrum:
                gap.append(energy[1] - energy[0])

            min_gap.append(min(gap))

        plt.plot(Nlist, min_gap, label=variables[0] + '=' + str(var))
    plt.yscale('log')

    plt.xlabel('system size $N$',fontsize=12)
    plt.ylabel('minimum energy gap $\Delta_{min}$',fontsize=12)
    plt.legend()
    plt.savefig(fig_path + 'gap' + filename_from(N, 1, params, system.params_name) + '.pdf')


