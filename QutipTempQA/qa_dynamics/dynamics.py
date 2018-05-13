import os
import pickle

from QutipTempQA.utils.utils import *

def dynamics_result(system ,N, T, param):
    file_path = "./data/evo_state/" + filename_from(N,T,param) + '.pickle'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            result = pickle.load(f)
        print('----- ' + file_path + ' success load file for dynamics.-----')
    else:
        print('****** ' + file_path + ' faild load file. calculating for dynamics ******')
        result = system.dynamics_mesolve(dt=0.01)
        with open(file_path, 'wb') as f:
            pickle.dump(result, f)

    return result.states[-1]