import numpy as np
import matplotlib.pyplot as plt

from QutipTempQA.utils.utils import plot_setting

def draw_energygap(fig_path, N, system, params, variable):

    plt.figure()
    plot_setting()

    for var in variable[1]:
        params[variable[0]] = var
        sys = system(T=1,N=N,param=params)

        gap = []
        tlist = np.arange(0,1.01,0.01)
        for t in tlist:
            spectrum = sys.H(t).eigenstates()[0]
            gap.append(spectrum[1] - spectrum[0])

        plt.plot(tlist,gap,label=variable[0]+'='+str(var))
    plt.legend()
    plt.savefig(fig_path+'energygap.pdf')