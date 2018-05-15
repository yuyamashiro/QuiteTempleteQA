import matplotlib.pyplot as plt


def plot_setting(font_size=8):
    plt.rcParams['font.family'] = 'sans-serif'  # 使用するフォント
    plt.rcParams['xtick.direction'] = 'in'  # x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
    plt.rcParams['ytick.direction'] = 'in'  # y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
    plt.rcParams['xtick.major.width'] = 1.0  # x軸主目盛り線の線幅
    plt.rcParams['ytick.major.width'] = 1.0  # y軸主目盛り線の線幅
    plt.rcParams['font.size'] = font_size  # フォントの大きさ
    plt.rcParams['axes.linewidth'] = 1.0  # 軸の線幅edge linewidth。囲みの太さ


def filename_from(N, T, param, names):
    filename = "N{}T{}".format(N,T)
    for key in names:
        filename += key+str(param[key]).replace(".","_")
    return filename