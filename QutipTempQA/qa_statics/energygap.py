import numpy as np
import matplotlib.pyplot as plt

from QutipTempQA.utils.utils import plot_setting
from QutipTempQA.utils.utils import filename_from

def draw_energygap(fig_path, N, system, params, variables):

    plt.figure()
    plot_setting()

    for var in variables[1]:
        params[variables[0]] = var
        sys = system(T=1,N=N,param=params)

        gap = []
        tlist = np.arange(0,1.01,0.01)
        for t in tlist:
            spectrum = sys.H(t).eigenstates()[0]
            gap.append(spectrum[1] - spectrum[0])

        plt.plot(tlist, gap, label=variables[0] + '=' + str(var))
    plt.legend()
    plt.savefig(fig_path+'gap' + filename_from(N,1,params,system.params_name) + '.pdf')
