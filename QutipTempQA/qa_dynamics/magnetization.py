import os
import numpy as np
from qutip import *

from .dynamics import *
from QutipTempQA.utils.utils import filename_from

class Magnetization:
    def __init__(self, system, N, T):
        self.system = system
        self.N = N
        self.T = T
        self.data_paths = []

    def calc_mag(self, params):
        data_path = './data/m_vs_t/mag_' + filename_from(self.N, self.T, params, self.system.params_name) + '.dat'
        if os.path.exists(data_path):
            print('load data of time evolution of magnetization')
            tlist ,mlist = np.loadtxt(data_path)
        else:
            print('**** calculate data of time evolution of magnetization ****')
            sys = self.system(self.T, self.N, params)
            results = dynamics_result(sys, self.N, self.T, params, only_final=False)
            mlist = [expect(sys.mz(), psi) for psi in results.states]
            with open(data_path, "ab") as f:
                np.savetxt(f, np.array([list(results.times), list(mlist)]))
        self.data_paths.append(data_path)

    def calc_magdist(self, params):
        data_path = './data/m_dist/m_dist_' + filename_from(self.N, self.T, params, self.system.params_name) + '.dat'
        if os.path.exists(data_path):
            print("load data of distribution of magnetization at final state")
        else:
            print("calculate distribution of magnetization at final state")
            sys = self.system(self.T, self.N, params)
            mz, m_basis = sys.mz().eigenstates()
            results = dynamics_result(sys, self.N, self.T, params)
            probs = [np.abs((mb.dag() * results).full()[0][0]) ** 2 for mb in m_basis]

            u_mz_prob = dict([[m, 0] for m in np.unique(mz)])
            for mag, p in zip(mz, probs):
                u_mz_prob[mag] += p

            mlist = list(u_mz_prob.keys())
            prob_list = list(u_mz_prob.values())
            with open(data_path, "ab") as f:
                np.savetxt(f, [mlist, prob_list])
        self.data_paths.append(data_path)

def calc_operator(results,operator):
    mlist = [expect(operator, psi) for psi in results]
    return mlist

