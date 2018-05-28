from QASystemClass import FullConnectSystem
from QutipTempQA import draw_eres_errorprob
from QutipTempQA import DynamicsEresError

def main():
    figure_paths = {'eres':"./figure/Eres/test.pdf",
                    'error_prob':"./figure/ErrorProb/jj.pdf"}
    N = 3
    Tlist = [1,10,30,50]

    plist = [3,5]

    # draw_eres_errorprob(
    #     figure_paths, N, Tlist,
    #     system=FullConnectSystem,
    #     params={},
    #     variables=['p', plist]
    # )

    eres_error = DynamicsEresError(FullConnectSystem, N, Tlist)
    for p in plist:
        params = {'p':p}
        eres_error.calculation(params=params, label='p={}'.format(p))
    eres_error.draw_results(figure_paths=figure_paths)


if __name__ == '__main__':
    import time
    start = time.time()

    main()

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
