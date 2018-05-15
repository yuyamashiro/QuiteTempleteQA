from qutip import *

from QutipTempQA import QASystem

class FullConnectSystem(QASystem):

    params_name = ['p']

    def __init__(self, T, N, param):

        self.T = T
        self.N = N
        self.p = param['p']

        # pre-allocate operators
        si = qeye(2)
        sx, sy, sz = sigmax(), sigmay(), sigmaz()
        self.sx_list, self.sy_list, self.sz_list = [], [], []

        for n in range(N):
            op_list = []
            for _ in range(N):
                op_list.append(si)

            op_list[n] = sx
            self.sx_list.append(tensor(op_list))

            op_list[n] = sy
            self.sy_list.append(tensor(op_list))

            op_list[n] = sz
            self.sz_list.append(tensor(op_list))


    def _dynamic_H(self):

        H0 = -self.N*(1.0/self.N * sum(self.sz_list))**self.p
        Vtf = -sum(self.sx_list)

        return [[H0, lambda t, args: t / self.T],
                [Vtf, lambda t, args: (1 - t/self.T)]]

    def mz(self):
        return 1.0/self.N * sum(self.sz_list)



