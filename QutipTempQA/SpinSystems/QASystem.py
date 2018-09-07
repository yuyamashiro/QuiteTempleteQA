from qutip import *
import numpy as np


class QASystem:
    def __init__(self, T):
        self.T = T

    def _dynamic_H(self):
        raise NotImplementedError('You should implemented "_dynamic_H()" at child class of QASystem')
        return

    def H(self,t):
        Ht = 0
        for hs in self._dynamic_H(): Ht += hs[0]*hs[1](t=t,args=0)
        return Ht

    def init_state(self):
        eigval, eigstat = self.H(0).eigenstates(sparse=False, eigvals=1)
        return eigstat[0]

    def dynamics_mesolve(self, dt, start=0):
        tlist = np.arange(start, self.T + dt, dt)
        return mesolve(self._dynamic_H(), self.init_state(), tlist, [], [], args={})


