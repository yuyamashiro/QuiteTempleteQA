import sys

import numpy as np
import matplotlib.pyplot as plt
from calculation import vs_N

def main(arg):
    if arg[0] == 'vsN':
        data_path = vs_N()
        Nlist, eres, error_p = np.loadtxt(data_path)

        plt.plot(Nlist, eres)
        plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])