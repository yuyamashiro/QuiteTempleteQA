from QASystemClass import FullConnectSystem
from QutipTempQA import draw_magnetization


def main():
    mag_figure_path = './figure/Magnetization/'

    N = 3
    T = 10

    draw_magnetization(
        mag_figure_path,
        N,T,
        system=FullConnectSystem,
        params={'p':3}
    )



if __name__ == '__main__':
    main()