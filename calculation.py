import sys
import numpy as np

from QutipTempQA import DynamicsEresError, OccupationProbability
from QASystemClass import BlockedSystem, FullConnectSystem

SYSTEM = BlockedSystem
p = 3

def main(args):
    system_class = BlockedSystem
    N = 100
    p = 3

    if args[0] == 'eres_prob':
        eres_prob()
    elif args[0] == 'energygap':
        draw_energygap(fig_path='./figure/minGap/',
                       system=system_class,
                       N=N,
                       params={'p':p},
                       variables=['p',[p]]
                       )
    elif args[0] == 'occ':
        occ()
    else:
        raise ValueError('{} is not defined.'.format(args[0]))

def eres_prob():
    N = 50
    p = 3
    Tlist = [1, 3, 5, 10, 30, 50, 100]
    params = {'p': p}
    eres_error = DynamicsEresError(BlockedSystem, N, Tlist, "blocked_pspin")
    eres_error.calculation(params=params, label='p={}'.format(p))
    return eres_error.data_paths, 'N{}p{}'.format(N,p)

def occ():
    p = 3
    N = 50
    T = 10
    M = 5
    params = {'p': p}
    occ_prob = OccupationProbability(SYSTEM, N, T, system_name="blocked_pspin")
    occ_prob.calculation(params=params, M=M)

    return occ_prob.tlist, occ_prob.evals_data_path, occ_prob.p_data_path, \
           {'N': N, 'T': T, 'M': M, 'params': params}, occ_prob.file_name

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
