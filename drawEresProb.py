from QASystemClass import FullConnectSystem
from QutipTempQA import draw_observables

def main():
    observables = {"Residual energy":"./figure/Eres/",
                  "Probability of mistaking":"./figure/MissProb/"}

    N = 3
    Tlist = [1,10,50]

    plist = [3,5]


    draw_observables(
        observables, N, Tlist,
        system= FullConnectSystem,
        params= {},
        variable= ['p', plist]
        )


if __name__ == '__main__':
    import time
    start = time.time()

    main()

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
