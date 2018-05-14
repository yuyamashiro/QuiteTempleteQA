from QASystemClass import FullConnectSystem
from QutipTempQA import draw_energygap


def main():
    gap_figure_path = './figure/EnergyGap/'

    N = 3
    plist = [3, 5]

    draw_energygap(
        gap_figure_path, N,
        system=FullConnectSystem,
        params={},
        variables=['p', plist]
    )



if __name__ == '__main__':
    main()