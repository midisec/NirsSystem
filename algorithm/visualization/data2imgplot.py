import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import io
import base64

#
# 返回值为图片的base64编码，预处理绘图show
# 丢进去的是 <class 'pandas.core.frame.DataFrame'> 类型数据  直接读csv文件直接丢进去
#
def draw_pic(data):

    img = io.BytesIO()
    n = data.shape[0]  # 样本数量
    spec_ = np.zeros_like(np.array(data))

    for i in range(n):
        spec_[i, :] = data.loc[i, :]
    plt.figure(figsize=(6.8, 3.8), dpi=400)
    x = [int(float(i)) for i in list(data.columns)]

    for i in range(n):
        plt.plot(x, spec_[i, :], linewidth=0.6)
        plt.xticks(x[::150])
        ax = plt.gca()
        x_major_locator = MultipleLocator(100)
        ax.xaxis.set_major_locator(x_major_locator)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.xlabel("Wavelength/nm")
    plt.ylabel("Reflectance")

    plt.title("源数据光谱曲线图")
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

def draw_pic_way(data, way):

    img = io.BytesIO()
    n = data.shape[0]  # 样本数量
    spec_ = np.zeros_like(np.array(data))

    for i in range(n):
        spec_[i, :] = data.loc[i, :]
    plt.figure(figsize=(6.8, 3.8), dpi=400)
    x = [int(float(i)) for i in list(data.columns)]

    for i in range(n):
        plt.plot(x, spec_[i, :], linewidth=0.6)
        plt.xticks(x[::150])
        ax = plt.gca()
        x_major_locator = MultipleLocator(100)
        ax.xaxis.set_major_locator(x_major_locator)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.xlabel("Wavelength/nm")
    plt.ylabel("Reflectance")

    plt.title(str(way) + "数据光谱曲线图")
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url
