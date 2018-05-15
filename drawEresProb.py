from QASystemClass import FullConnectSystem
from QutipTempQA import draw_eres_errorprob

def main():
    figure_paths = {'eres':"./figure/Eres/",
                    'error_prob':"./figure/ErrorProb/"}
    N = 3
    Tlist = [1,10,50]

    plist = [3,5]

    draw_eres_errorprob(
        figure_paths, N, Tlist,
        system=FullConnectSystem,
        params={},
        variables=['p', plist]
    )


if __name__ == '__main__':
    import time
    start = time.time()

    main()

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
