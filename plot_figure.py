import sys

import numpy as np
import matplotlib.pyplot as plt

from QutipTempQA.utils import utils
from calculation import vs_N, occ, eres_prob

def main(arg):
    if arg[0] == 'eres_prob':
        data_path, param_name = eres_prob()
        Tlist, eres, errorprob, tts = np.loadtxt(data_path)

        eresprob_draw(fig_path='./figure/Eres/eres_'+ param_name + '.pdf', tlist=Tlist, data=eres)
        eresprob_draw(fig_path='./figure/ErrorProb/eprob_' + param_name + '.pdf', tlist=Tlist, data=errorprob)
        eresprob_draw(fig_path='./figure/TTS/tts_' + param_name + '.pdf', tlist=Tlist, data=tts)

    elif arg[0] == 'vsN':
        data_path = vs_N()
        Nlist, eres, error_p = np.loadtxt(data_path)

        plt.plot(Nlist, eres)
        plt.show()
    elif arg[0] == 'occ':
        tlist, evals_path, prob_path, params, file_name = occ()

        print('---plotting start!---')

        evals_data = np.loadtxt(evals_path)
        prob_data = np.loadtxt(prob_path)

        fig_path = './figure/OccProb/'
        occ_draw(
            fig_path=fig_path,
            tlist=tlist, evals_mat=evals_data, P_mat=prob_data,
            M=params['M'], N=params['N'], file_name=file_name
        )
        print('--done--')

def eresprob_draw(fig_path, tlist, data):
    utils.plot_setting(font_size=10)
    plt.plot(tlist, data)
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig(fig_path)


def occ_draw(fig_path, tlist, evals_mat, P_mat, M, N, file_name):

    utils.plot_setting(font_size=10)

    # first draw thin lines outlining the energy spectrum
    for n in range(len(evals_mat)):
        ls,lw = ('b', 1) if n == 0 else ('k', 0.25)
        plt.plot(tlist, evals_mat[n], ls, lw=lw)

    # second, draw line that encode the occupation probability of each state in
    # its linewidth. thicker line => high occupation probability.
    for idx in range(len(tlist)-1):
        for n in range(len(P_mat)):
            lw = 0.5 + 4*P_mat[n,idx]
            if lw > 0.55:
                plt.plot([tlist[idx], tlist[idx+1]],
                          [evals_mat[n, idx], evals_mat[n, idx+1]],
                           'r', lw=lw)

    plt.ylabel('Energies')
    plt.xlabel('t')
    plt.title('Energyspectrum ({} lowest values) of {} spins.\n'.format(M, N)
              + 'The occupation probabilities are encode in the red line widths.')

    file_name = fig_path + file_name + '.pdf'
    plt.savefig(file_name)

if __name__ == '__main__':
    main(sys.argv[1:])