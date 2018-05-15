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
        data_path = "./data/eres_errorprop/" + filename_from(N, '_', allparams)
        if os.path.exists(data_path):
            prot_Tlist, eres, errorprop = calc_otherT_eres_errorprop(data_path, N, Tlist, system, allparams)
        else:
            plot_Tlist = Tlist
            eres, errorprop = calc_eres_errorprop(N, Tlist, system, allparams)

        eres_mat.append(eres)
        errorprop_mat.append(errorprop)

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




def draw_observables(observables, N, Tlist, system, params, variables, draw=True):
    # dictionary( values type is 2d array ) of result of observables that is specified
    result_obs = {}
    calculated_Tlist = {}
    for key, _ in observables.items():
        result_obs[key] = []

    for var in variables[1]:
        allparams = params
        allparams[variables[0]] = var

        for obs,_ in observables.items():
            obs_results = load_data(obs,N,allparams)
            if obs_results is not None:
                calculated_Tlist[obs] = obs_results[0]
                result_obs[key] = obs_results[1]

                will_calc_Tlist = list(set(Tlist) - set(calculated_Tlist))





    # result_obs have 2d-array(matrix) 1-axis : each T, 2-axis : each variable
    # follow two for statement is doing stuck result to result_obs
    for i,var in enumerate(variables[1]):
        obs_eachT = {}
        for key,_ in observables.items():
            obs_eachT[key] = []

        for T in Tlist:
            allparams = params
            allparams[variables[0]] = var

            sys = system(T, N, allparams)
            results = dynamics_result(sys, N, T, allparams)
            final_state = results[-1]

            correct_energy, correct_state = sys.H(T).eigenstates(eigvals=1)

            # calculate observables
            for obs, path in observables.items():
                if obs == "Residual energy":
                    Eres = 1.0 / sys.N * np.abs(expect(sys.H(T), final_state) - correct_energy[0])
                    obs_eachT[obs].append(Eres)
                elif obs == "Probability of mistaking":
                    miss_prob = 1.0 - np.abs((correct_state[0].dag() * final_state).full()[0][0]) ** 2
                    obs_eachT[obs].append(miss_prob)
                else:
                    raise ValueError("Observable {} is not exist".format(obs))

        for key, value in obs_eachT.items():
            result_obs[key].append(value)
            save_to_data(key, value, Tlist, N, allparams)

    # draw figure of result vs T
    if draw :
        for obs, path in observables.items():
            draw_to_figure(obs, path, result_obs[obs], Tlist, N, params, variables)

def save_to_data(observable, result_data, Tlist, N, allparams):
    if observable == "Residual energy":
        obs_name = 'Eres/'
    elif observable == "Probability of mistaking":
        obs_name = 'MisProb/'
    else:
        raise ValueError("Observable {} is not exist".format(obs))
    data_path = './data/'+ obs_name + filename_from(N, T='_',param=allparams) + '.dat'
    np.savetxt(data_path,np.array([Tlist,result_data]))


def load_data(observable, N, allparams):
    if observable == "Residual energy":
        obs_name = 'Eres/'
    elif observable == "Probability of mistaking":
        obs_name = 'MisProb/'
    else:
        raise ValueError("Observable {} is not exist".format(obs))
    data_path = './data/' + obs_name + filename_from(N, T='_', param=allparams) + '.dat'
    if os.path.exists(data_path):
        return np.loadtxt(data_path)
    else:
        return None


def draw_to_figure(observable, path, result_mat, Tlist, N, params, variable):
    T = max(Tlist)
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



