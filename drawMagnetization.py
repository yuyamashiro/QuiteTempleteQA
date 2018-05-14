from QASystemClass import FullConnectSystem
from QutipTempQA import draw_magnetization


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



if __name__ == '__main__':
    main()