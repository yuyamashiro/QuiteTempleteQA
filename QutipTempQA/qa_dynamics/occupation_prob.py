import numpy as np
from qutip import *

from .dynamics import *


class OccupationProbability:
    def __init__(self, system, N, T):
        self.system = system
        self.evals_mat = []
        self.P_mat = []

        self.N = N
        self.T = T
        self.tlist = np.arange(0, T+0.01, 0.01)

        self.M = 0

        self.file_name = ''

    def calculation(self, params, M):

        self.file_name = filename_from(self.N, self.T,
                                       param=params, names=self.system.params_name) + 'M_' + str(M)

        evals_data_path = './data/occ_prob/'+'evals_'+self.file_name+'.dat'
        p_data_path = './data/occ_prob/' + 'p_' + self.file_name + '.dat'

        if os.path.exists(evals_data_path) and os.path.exists(p_data_path):
            print('success load {}'.format(self.file_name))
            self.evals_mat = np.loadtxt(evals_data_path)
            self.P_mat = np.loadtxt(p_data_path)
        else:
            print('*** calculate ***')
            self.calc_evals_Pmat(params, M)
            np.savetxt(evals_data_path, self.evals_mat)
            np.savetxt(p_data_path, self.P_mat)



    def calc_evals_Pmat(self, params, M):

        self.M = M
        sys = self.system(self.N, self.T, params)

        self.evals_mat = []
        self.P_mat = []

        results = dynamics_result(system=sys, N=self.N, T=self.T, param=params, only_final=False)

        for t, psi in zip(results.times, results.states):
            # find the M lowest eigenvalues of the system
            evals, ekets = sys.H(t).eigenstates(eigvals=M)

            self.evals_mat.append(list(evals))

            self.P_mat.append([])
            for eket in ekets:
                self.P_mat[-1].append(np.abs((eket.dag().data * psi.data)[0, 0]) ** 2)

        self.evals_mat = np.array(self.evals_mat).T
        self.P_mat = np.array(self.P_mat).T

    def draw(self, fig_path):

        plot_setting(font_size=10)

        # first draw thin lines outlining the energy spectrum
        for n in range(len(self.evals_mat)):
            ls,lw = ('b', 1) if n == 0 else ('k', 0.25)
            plt.plot(self.tlist, self.evals_mat[n], ls, lw=lw)

        # second, draw line that encode the occupation probability of each state in
        # its linewidth. thicker line => high occupation probability.
        for idx in range(len(self.tlist)-1):
            for n in range(len(self.P_mat)):
                lw = 0.5 + 4*self.P_mat[n,idx]
                if lw > 0.55:
                    plt.plot([self.tlist[idx],self.tlist[idx+1]],
                              [self.evals_mat[n, idx], self.evals_mat[n, idx+1]],
                               'r', lw=lw)

        plt.ylabel('Energies')
        plt.xlabel('t')
        plt.title('Energyspectrum ({} lowest values) of {} spins.\n'.format(self.M, self.N)
                  + 'The occupation probabilities are encode in the red line widths.')

        file_name = fig_path + self.file_name
        plt.savefig(file_name)





