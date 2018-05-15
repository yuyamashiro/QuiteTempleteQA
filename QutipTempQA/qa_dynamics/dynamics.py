import os
import pickle

from QutipTempQA.utils.utils import *

def dynamics_result(system ,N, T, param):

    file_path = "./data/evo_state/N{}".format(N)
    os.makedirs(file_path, exist_ok=True)

    file_path += "/" + filename_from(N, T, param, system.params_name) + '.pickle'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            result = pickle.load(f)
        print('----- ' + file_path + ' success load file for dynamics.-----')
    else:
        print('****** ' + file_path + ' faild load file. calculating for dynamics ******')
        result = system.dynamics_mesolve(dt=0.01)
        with open(file_path, 'wb') as f:
            pickle.dump(result, f)

    return result.states