from QASystemClass import BlockedSystem
from QutipTempQA import OccupationProbability


def main():
    fig_path = './figure/OccProb/'
    N = 10
    T = 10
    p = 3
    occ_prob = OccupationProbability(BlockedSystem, N, T)
    occ_prob.calculation(params={'p': p}, M=5)
    occ_prob.draw(fig_path)


if __name__ == '__main__':
    main()