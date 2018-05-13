# Qutip Templete for Quantum annealing(QA) simulation

## Directory structure

```
.
├── README.md
├── QutipTempQA
│   ├── SpinSystems
│   ├── qa_dynamics
│   ├── qa_statics
│   └── utils
├── QASystemClass.py
├── drawEnergyGap.py
├── drawEresProb.py
├── data
│   └── evo_state
└── figure
    ├── EnergyGap
    ├── Eres
    └── MissProb 
```

## Example Codes

Example codes are configured follow tree python files.

- QASystemClass.py  
    This is written information of system hamiltonian.
- drawEnergyGap.py  
- drawEresProb.py

## How to use

1. Make directory for save data.  
Dynamics result are saved in `/data/evo_state` 
(data directory in the same directory at call draw function.).  
However figures directory are not restrict, 
you can choice at argument of draw functions(detail follow step ``3. Call draw function``).

2. Make System Hamiltonian Class in the same directory layer
as 'QutipTempQA' directory  
    See ``QASystemClass.py``. 
    System hamiltonian class should inheritance 
    ``QutipTempQA.QASystem`` and should override 
    ``_dynamic_H()``.  
    
    > _dynamic_H() return list of list which  
     [matrix of hamiltonian, time dependent function as coefficient]
     
    And argument __init__ function is should implement
    ```python
    __init__(self,T, N, param)
    ```
    which ``param`` is dictionary of parameters.
     See ``QASystemClass.py`` for detail.
     
 3. Call draw function  
 If you want value of result of QA dynamics,
  call ``draw_observables()``.
 If you want value of energy gap, call ``draw_energygap()``.  
 See ``drawEresProb.py`` or ``drawEnergyGap.py`` for detail.
