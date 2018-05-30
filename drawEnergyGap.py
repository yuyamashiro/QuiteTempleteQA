from QASystemClass import FullConnectSystem
from QASystemClass import BlockedSystem
from QutipTempQA import draw_energygap, draw_min_gap


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

    mingap_fig_path = './figure/mingap/'
    draw_min_gap(
        mingap_fig_path,
        Nlist=[3,5,10,15,20,30,40,50,55],
        system=BlockedSystem,
        params={},
        variables=['p',plist]
    )


if __name__ == '__main__':
    main()
