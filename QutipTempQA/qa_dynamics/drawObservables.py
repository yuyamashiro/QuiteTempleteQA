import os
import numpy as np
from qutip import *
import matplotlib.pyplot as plt

from QutipTempQA.utils.utils import *
from .dynamics import dynamics_result

class DynamicsEresError:
    def __init__(self, system, N, Tlist):
        self.system = system
        self.N = N
        self.Tlist = Tlist
        self.eres_mat = []
        self.errorprob_mat = []
        self.label_list = []

    def calculation(self, params, label):
        data_path = "./data/eres_errorprob/" + filename_from(self.N, '_', params, names=self.system.params_name) + ".dat"
        if os.path.exists(data_path):
            print('load data of residual energy and error probability at parameters {}'.format(params))
            plot_Tlist, eres, errorprob = calc_otherT_eres_errorprob(data_path, self.N, self.Tlist, self.system, params)

            np.savetxt(data_path, [plot_Tlist, eres, errorprob])

            # choice only Tlist data
            Tlist_arg = [np.where(plot_Tlist == t)[0][0] for t in self.Tlist]
            eres = eres[Tlist_arg]
            errorprob = errorprob[Tlist_arg]

        else:
            print('never have been calculated parameters {}. calculating...'.format(params))
            eres, errorprob = calc_eres_errorprob(self.N, self.Tlist, self.system, params)
            np.savetxt(data_path, np.array([self.Tlist, eres, errorprob]))

        self.eres_mat.append(eres)
        self.errorprob_mat.append(errorprob)
        self.label_list.append(label)

    def draw_results(self,figure_paths):
        print("draw and save as figure")
        self.draw_save_to('Residual energy', figure_paths['eres'], self.eres_mat, self.Tlist, self.label_list)
        self.draw_save_to('Error probability', figure_paths['error_prob'], self.errorprob_mat, self.Tlist, self.label_list)

    def draw_save_to(self, obs_name, fig_path, result_mat, Tlist, label_list):

        plt.figure()
        plot_setting(font_size=10)
        plt.xlabel("$T_{QA}$ : Annealing time", fontsize=12)
        plt.ylabel(obs_name, fontsize=12)
        plt.xscale('log')
        plt.yscale('log')

        for label, result in zip(label_list, result_mat):
            plt.plot(Tlist, result, label=label)

        plt.legend()
        plt.savefig(fig_path, bbox_inches="tight", pad_inches=0.0)




def draw_eres_errorprob(figure_paths, N, Tlist, system, params, variables, draw=True):

    eres_mat = []
    errorprob_mat = []
    for var in variables[1]:
        allparams = params
        allparams[variables[0]] = var
        data_path = "./data/eres_errorprob/" + filename_from(N, '_', allparams, names=system.params_name) + ".dat"
        if os.path.exists(data_path):
            print('load data of residual energy and error probability at parameters {}'.format(allparams))
            plot_Tlist, eres, errorprob = calc_otherT_eres_errorprob(data_path, N, Tlist, system, allparams)

            np.savetxt(data_path, [plot_Tlist, eres, errorprob])

            # choice only Tlist data
            Tlist_arg = [np.where(plot_Tlist == t)[0][0] for t in Tlist]
            eres = eres[Tlist_arg]
            errorprob = errorprob[Tlist_arg]

        else:
            print('never have been calculated parameters {}. calculating...'.format(allparams))
            eres, errorprob = calc_eres_errorprob(N, Tlist, system, allparams)
            np.savetxt(data_path, np.array([Tlist, eres, errorprob]))

        eres_mat.append(eres)
        errorprob_mat.append(errorprob)


    if draw:
        draw_to_figure('Residual energy', figure_paths['eres'], eres_mat, Tlist,
                       N, params, variables, system.params_name)
        draw_to_figure('Error probability', figure_paths['error_prob'], errorprob_mat, Tlist,
                       N, params, variables, system.params_name)


def calc_otherT_eres_errorprob(data_path, N, Tlist, system, allparams):
    calculated_Tlist, eres, errorprob = np.loadtxt(data_path)
    will_calc_Tlist = list(set(Tlist) - set(calculated_Tlist))

    new_eres, new_errorprob = calc_eres_errorprob(N, will_calc_Tlist, system, allparams)

    eres = np.append(eres, new_eres)
    errorprob = np.append(errorprob, new_errorprob)
    new_Tlist = np.append(calculated_Tlist, will_calc_Tlist)

    sorted_arg_Tlist = new_Tlist.argsort()

    return new_Tlist[sorted_arg_Tlist], eres[sorted_arg_Tlist], errorprob[sorted_arg_Tlist]


def calc_eres_errorprob(N, Tlist, system, allparams):
    eres = []
    errorprob = []
    for T in Tlist:
        sys = system(T, N, allparams)
        final_state = dynamics_result(sys, N, T, allparams)
        correct_energy, correct_state = sys.H(T).eigenstates(eigvals=1)

        eres.append(1.0 / sys.N * np.abs(expect(sys.H(T), final_state) - correct_energy[0]))
        errorprob.append(1.0 - np.abs((correct_state[0].dag() * final_state).full()[0][0]) ** 2)

    return eres, errorprob




def draw_to_figure(observable, path, result_mat, Tlist, N, params, variable, params_name):
    T = int(max(Tlist))
    figure_path = path + filename_from(N, T, params, names=params_name) + '.pdf'

    plt.figure()
    plot_setting(font_size=10)
    plt.xlabel("$T_{QA}$ : Annealing time", fontsize=12)
    plt.ylabel(observable, fontsize=12)
    plt.xscale('log')
    plt.yscale('log')

    for value, result in zip(variable[1], result_mat):
        plt.plot(Tlist, result, label=variable[0]+"="+str(value))

    plt.legend()
    plt.savefig(figure_path, bbox_inches="tight", pad_inches=0.0)



