import os
import numpy as np
from qutip import *

from QutipTempQA.utils.utils import *
from .dynamics import dynamics_result

class DynamicsEresError:
    def __init__(self, system, N, Tlist):
        self.system = system
        self.N = N
        self.Tlist = Tlist
        self.eres_mat = []
        self.errorprob_mat = []
        self.tts_mat = []
        self.label_list = []
        self.data_paths = []

    def calculation(self, params, label):
        data_path = "./data/eres_errorprob/" + filename_from(self.N, '_', params, names=self.system.params_name) + ".dat"
        if os.path.exists(data_path):
            print('load data of {}'.format(data_path))
            plot_Tlist, eres, errorprob, tts = calc_otherT_eres_errorprob(data_path, self.N, self.Tlist, self.system, params)

            np.savetxt(data_path, [plot_Tlist, eres, errorprob, tts])

            # choice only Tlist data
            Tlist_arg = [np.where(plot_Tlist == t)[0][0] for t in self.Tlist]
            eres = eres[Tlist_arg]
            errorprob = errorprob[Tlist_arg]
            tts = tts[Tlist_arg]

        else:
            print('never have been calculated parameters {}. calculating...'.format(params))
            eres, errorprob, tts = calc_eres_errorprob(self.N, self.Tlist, self.system, params)
            np.savetxt(data_path, np.array([self.Tlist, eres, errorprob, tts]))

        self.data_paths.append(data_path)
        self.eres_mat.append(eres)
        self.errorprob_mat.append(errorprob)
        self.tts_mat.append(tts)
        self.label_list.append(label)


def calc_otherT_eres_errorprob(data_path, N, Tlist, system, allparams):
    calculated_Tlist, eres, errorprob, tts = np.loadtxt(data_path)
    if not hasattr(calculated_Tlist, '__iter__'):
        calculated_Tlist = [calculated_Tlist]
    will_calc_Tlist = list(set(Tlist) - set(calculated_Tlist))

    new_eres, new_errorprob, new_tts = calc_eres_errorprob(N, will_calc_Tlist, system, allparams)

    eres = np.append(eres, new_eres)
    errorprob = np.append(errorprob, new_errorprob)
    tts = np.append(tts, new_tts)
    new_Tlist = np.append(calculated_Tlist, will_calc_Tlist)

    sorted_arg_Tlist = new_Tlist.argsort()

    return new_Tlist[sorted_arg_Tlist], eres[sorted_arg_Tlist], errorprob[sorted_arg_Tlist], tts[sorted_arg_Tlist]


def calc_eres_errorprob(N, Tlist, system, allparams):
    eres = []
    errorprob = []
    tts = []
    pd = 0.99
    for T in Tlist:
        sys = system(T, N, allparams)
        final_state = dynamics_result(sys, N, T, allparams)
        correct_energy, correct_state = sys.H(T).eigenstates(eigvals=1)

        eres.append(1.0 / sys.N * np.abs(expect(sys.H(T), final_state) - correct_energy[0]))

        success_prob = np.abs((correct_state[0].dag() * final_state).full()[0][0]) ** 2
        errorprob.append(1.0 - success_prob)
        tts.append(T*np.log(1.0 - pd)/np.log(1-success_prob))

    return eres, errorprob, tts



