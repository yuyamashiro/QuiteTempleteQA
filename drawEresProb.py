from QASystemClass import FullConnectSystem
from QutipTempQA import draw_eres_errorprop

def main():
    figure_paths = {'eres':"./figure/Eres/",
                    'error_prop':"./figure/ErrorProp/"}
    N = 3
    Tlist = [1,10,50]

    plist = [3,5]

    draw_eres_errorprop(
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
