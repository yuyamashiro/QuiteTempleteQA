import os
import numpy as np

from QutipTempQA.utils.utils import filename_from

class EnergyGap:
    def __init__(self, system, N):
        self.system = system
        self.N = N
        self.data_paths = []

    def calculation(self, params):
        data_path = "./data/spectrum/spect_" + filename_from(self.N, '_', params, names=self.system.params_name) + ".dat"
        tlist = np.arange(0, 1.01, 0.01)
        if os.path.exists(data_path):
            print("-- {} is exist -- will load".format(data_path))
        else:
            print("*** {} is not exist *** calculating ...".format(data_path))
            sys = self.system(T=1, N=self.N, param=params)
            spectrum = []
            for t in tlist:
                spectrum.append(sys.H(t).eigenstates()[0])
            np.savetxt(data_path, spectrum)
        self.data_paths.append(data_path)


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


def draw_gapmap(fig_path, N, system, params, slist, newparam_list, axis_label, ticks=None):
    all_param = params.copy()
    gap_mat = []
    data_path = "./data/gap_mat/gapmat_" + filename_from(N, '_', params, names=system.params_name) + ".dat"

    if os.path.exists(data_path):
        print("-- {} is exist -- will load".format(data_path))
        gap_mat = np.loadtxt(data_path)
    else:
        for nparam in newparam_list[1]:
            all_param[newparam_list[0]] = nparam
            sys = system(T=1, N=N, param=all_param)
            spectrum = []
            for s in slist:
                spectrum.append(sys.H(s).eigenstates()[0])
            spectrum = np.array(spectrum).T
            gap_mat.append(spectrum[1] - spectrum[0])
        np.savetxt(data_path, gap_mat)

    plot_setting(font_size=10)
    if ticks is None:
        plt.xticks(range(0, 110, 10), np.arange(0, 1.1, 0.1))
        plt.yticks(range(0, 110, 10), np.arange(0, 1.1, 0.1)[::-1])
    else:
        plt.xticks(ticks['x'][0], ticks['x'][1])
        plt.xticks(ticks['y'][0], ticks['y'][1])
    plt.xlabel(axis_label[0])
    plt.ylabel(axis_label[1])
    plt.imshow(np.array(gap_mat).T[::-1])
    plt.savefig(fig_path + 'gapmat_' + filename_from(N, '_', params, names=system.params_name) + ".pdf")

