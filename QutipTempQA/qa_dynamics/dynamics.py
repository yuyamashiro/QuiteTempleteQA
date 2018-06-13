import os
import pickle

from QutipTempQA.utils.utils import *

def dynamics_result(system ,N, T, param, only_final=True):

    file_path = "./data/evo_state/N{}".format(N)
    os.makedirs(file_path, exist_ok=True)

    file_path += "/finalstate_" + filename_from(N, T, param, system.params_name) + '.pickle'
    if os.path.exists(file_path) and only_final:
        with open(file_path, 'rb') as f:
            final_state = pickle.load(f)
        print('----- ' + file_path + ' success load file for dynamics.-----')
    else:
        print('****** ' + file_path + ' faild load file. calculating for dynamics ******')
        result = system.dynamics_mesolve(dt=0.01)

        final_state = result.states[-1]
        with open(file_path, 'wb') as f:
            pickle.dump(final_state, f)

        if not only_final:
            return result

    return final_state