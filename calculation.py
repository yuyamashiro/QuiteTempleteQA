import sys
import numpy as np

from QutipTempQA import DynamicsEresError, draw_energygap, OccupationProbability
from QASystemClass import BlockedSystem, FullConnectSystem


def main(args):
    system_class = BlockedSystem
    N = 100
    p = 3

    if args[0] == 'dynamics':
        Tlist = [1,5,10]
        dynamics(system_class, N, Tlist, p)
    elif args[0] == 'energygap':
        draw_energygap(fig_path='./figure/minGap/',
                       system=system_class,
                       N=N,
                       params={'p':p},
                       variables=['p',[p]]
                       )
    elif args[0] == 'occ':
        fig_path = './figure/OccProb/'
        T = 10
        occ_prob = OccupationProbability(system=system_class, N=N, T=T)
        occ_prob.calculation(params={'p': p}, M=5)
        occ_prob.draw(fig_path)
    else:
        raise ValueError('{} is not defined.'.format(args[0]))


def dynamics(system_class, N, Tlist, p):
    eres_error = DynamicsEresError(system_class, N, Tlist)
    params = {'p': p}
    eres_error.calculation(params=params, label='up:{}'.format(up))

    observables = {"eres": "./figure/eres/eres_N{}p{}".format(N, p) + ".pdf",
                   "error_prob": "./figure/errorprob/error_N{}p{}".format(N, p) + ".pdf",
                   "tts": "./figure/TTS/tts_N{}p{}".format(N, p) + ".pdf"}

    eres_error.draw_results(observables)

def vs_N():
    system_class = BlockedSystem
    Nlist = [3,5,7,9,11,13,15,17,19,21]
    T = 100
    p = 3


    dynamics = DynamicsEresError(system=system_class, N=Nlist[0], Tlist=[T])
    for N in Nlist:
        dynamics.N = N
        dynamics.calculation(params={'p':p}, label='N={}'.format(N))
    eres_mat = np.array(dynamics.eres_mat).reshape((len(dynamics.eres_mat),))  # Nlist[Tlist[]]
    ep_mat = np.array(dynamics.errorprob_mat).reshape((len(dynamics.errorprob_mat, )))

    data_path = './data/vsN/p{}_vs_N.dat'.format(p)
    np.savetxt(data_path, [Nlist, eres_mat, ep_mat])

    return data_path


if __name__ == '__main__':
    main(sys.argv[1:])
