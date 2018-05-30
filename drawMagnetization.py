from QASystemClass import FullConnectSystem, BlockedSystem
from QutipTempQA import draw_magnetization
from QutipTempQA import draw_dist_magnetization


def main():
    mag_figure_path = './figure/Magnetization/'

    N = 3
    T = 10
    plist = [3,5]

    draw_magnetization(
        mag_figure_path,
        N,T,
        system=FullConnectSystem,
        params={},
        variables=['p',plist]
    )

    N = 45
    dist_figure_path = './figure/mag_dist/'
    draw_dist_magnetization(
        dist_figure_path,
        N,T,
        system=BlockedSystem,
        params={'p':plist[0]},
        bar_width=0.05
    )



if __name__ == '__main__':
    main()