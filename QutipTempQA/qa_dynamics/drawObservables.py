import os
import numpy as np
from qutip import *
import matplotlib.pyplot as plt

from QutipTempQA.utils.utils import *
from .dynamics import dynamics_result


def draw_eres_errorprop(figure_paths, N, Tlist, system, params, variables, draw=True):

    eres_mat = []
    errorprop_mat = []
    for var in variables[1]:
        allparams = params
        allparams[variables[0]] = var
        data_path = "./data/eres_errorprop/" + filename_from(N, '_', allparams) + ".dat"
        if os.path.exists(data_path):
            print('load data of residual energy and error probability at parameters {}'.format(allparams))
            plot_Tlist, eres, errorprop = calc_otherT_eres_errorprop(data_path, N, Tlist, system, allparams)
        else:
            print('never have been calculated parameters {}. calculating...'.format(allparams))
            plot_Tlist = Tlist
            eres, errorprop = calc_eres_errorprop(N, Tlist, system, allparams)

        eres_mat.append(eres)
        errorprop_mat.append(errorprop)

        save_to_data(eres, errorprop, Tlist, N, allparams)

    if draw:
        draw_to_figure('Residual energy', figure_paths['eres'], eres_mat, plot_Tlist, N, params, variables)
        draw_to_figure('Error probability', figure_paths['error_prop'], errorprop_mat, plot_Tlist, N, params, variables)


def calc_otherT_eres_errorprop(data_path, N, Tlist, system, allparams):
    calculated_Tlist, eres, errorprop = np.loadtxt(data_path)

    will_calc_Tlist = list(set(Tlist) - set(calculated_Tlist))

    new_eres, new_errorprob = calc_eres_errorprop(N, will_calc_Tlist, system, allparams)

    eres = np.append(eres, new_eres)
    errorprop = np.append(errorprop, new_errorprob)
    new_Tlist = np.append(calculated_Tlist, will_calc_Tlist)

    sorted_arg_Tlist = new_Tlist.argsort()

    return new_Tlist[sorted_arg_Tlist], eres[sorted_arg_Tlist], errorprop[sorted_arg_Tlist]


def calc_eres_errorprop(N, Tlist, system, allparams):
    eres = []
    errorprob = []
    for T in Tlist:
        sys = system(T, N, allparams)
        results = dynamics_result(sys, N, T, allparams)
        final_state = results[-1]
        correct_energy, correct_state = sys.H(T).eigenstates(eigvals=1)

        eres.append(1.0 / sys.N * np.abs(expect(sys.H(T), final_state) - correct_energy[0]))
        errorprob.append(1.0 - np.abs((correct_state[0].dag() * final_state).full()[0][0]) ** 2)

    return eres, errorprob



def save_to_data(eres, errorprop, Tlist, N, allparams):
    data_path = './data/eres_errorprop/' + filename_from(N, T='_',param=allparams) + '.dat'
    np.savetxt(data_path,np.array([Tlist,eres, errorprop]))


def draw_to_figure(observable, path, result_mat, Tlist, N, params, variable):
    T = int(max(Tlist))
    figure_path = path + filename_from(N, T, params) + '.pdf'

    plt.figure()
    plot_setting()
    plt.xlabel("$T_{Q}$ : Annealing time")
    plt.ylabel(observable)
    plt.xscale('log')
    plt.yscale('log')

    for value, result in zip(variable[1], result_mat):
        plt.plot(Tlist, result, label=variable[0]+"="+str(value))

    plt.legend()
    plt.savefig(figure_path)



