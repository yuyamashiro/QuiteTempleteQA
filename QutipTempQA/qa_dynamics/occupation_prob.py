import numpy as np
from qutip import *

from .dynamics import *


class OccupationProbability:
    def __init__(self, system, N, T, system_name):
        self.system = system
        self.evals_mat = []
        self.P_mat = []

        self.N = N
        self.T = T

        self.M = 0

        self.file_name = ''

        self.evals_data_path = ''
        self.p_data_path = ''

        self.system_name = system_name

    def calculation(self, params, M):

        self.file_name = filename_from(self.N, self.T,
                                       param=params, names=self.system.params_name) + 'M_' + str(M)

        file_path = "./data/occ_prob/{}/".format(self.system_name) + self.file_name
        os.makedirs(file_path, exist_ok=True)

        self.evals_data_path = file_path +'/evals_'+self.file_name+'.dat'
        self.p_data_path = file_path + '/p_' + self.file_name + '.dat'
        self.t_data_path = file_path + '/t_'+self.file_name + '.dat'

        if os.path.exists(self.evals_data_path) and os.path.exists(self.p_data_path):
            print('success load {}'.format(self.file_name))
            self.evals_mat= np.loadtxt(self.evals_data_path)
            self.tlist = np.loadtxt(self.t_data_path)
            self.P_mat = np.loadtxt(self.p_data_path)
        else:
            print('*** calculate ***')
            self.tlist = self.calc_evals_Pmat(params, M, self.system_name)
            np.savetxt(self.evals_data_path, self.evals_mat)
            np.savetxt(self.t_data_path, self.tlist)
            np.savetxt(self.p_data_path, self.P_mat)


    def calc_evals_Pmat(self, params, M, system_name):

        self.M = M
        sys = self.system(self.N, self.T, params)

        self.evals_mat = []
        self.P_mat = []

        results = dynamics_result(system=sys, N=self.N, T=self.T, param=params,
                                  system_name=system_name, only_final=False)
        for t, psi in zip(results.times, results.states):
            # find the M lowest eigenvalues of the system
            evals, ekets = sys.H(t).eigenstates(eigvals=M)

            self.evals_mat.append(list(evals))

            self.P_mat.append([])
            for eket in ekets:
                self.P_mat[-1].append(np.abs((eket.dag().data * psi.data)[0, 0]) ** 2)

        self.evals_mat = np.array(self.evals_mat).T
        self.P_mat = np.array(self.P_mat).T

        return results.times


