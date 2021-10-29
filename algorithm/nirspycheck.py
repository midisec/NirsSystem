import config
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import math
from algorithm.visualization.data2imgplot import draw_pic_way

class NirspyCheck(object):
    def __init__(self, modelfolder='default'):
        self.modelfolder = config.MODELS_PATH + modelfolder

    def conf_load(self):
        with open("{}/models/config.data".format(self.modelfolder), "rb") as f:
            return pickle.load(f)

    def assessment_handler(self):
        result = self.conf_load()
        # for i in result:
        #     print(i)

        sorted_result = sorted(result, key=lambda result : result['test']['rpd'], reverse=True)
        # print(sorted_result)
        # for i in sorted_result:
        #     print(i)
        # print("[*] 最优的模型组合为：{}+{}, 其中rpd：{}、rmse：{}、r2：{}".format(sorted_result[0]['pre_way'], sorted_result[0]['model'], sorted_result[0]['test']['rpd'], sorted_result[0]['test']['rmse'], sorted_result[0]['test']['r2']))

        return sorted_result[0]['pre_way'],  sorted_result[0]['model']

    def pretreatment_handler(self, data, way):
        """
            多种预处理
        :param data:
        :return:
        """

        # ----------------------------------------SG----------------------------------------
        def create_x(size, rank):
            x = []
            for i in range(2 * size + 1):
                m = i - size
                row = [m ** j for j in range(rank)]
                x.append(row)
            x = np.mat(x)
            return x

        def sg(data_x, window_size, rank):
            """
             * Savitzky-Golay平滑滤波函数
             * data - list格式的1×n纬数据
             * window_size - 拟合的窗口大小
             * rank - 拟合多项式阶次
             * ndata - 修正后的值
            """
            m = int((window_size - 1) / 2)
            odata = data_x[:]
            for i in range(m):
                odata.insert(0, odata[0])
                odata.insert(len(odata), odata[len(odata) - 1])
            x = create_x(m, rank)
            b = (x * (x.T * x).I) * x.T
            a0 = b[m]
            a0 = a0.T
            ndata = []
            for i in range(len(data_x)):
                y = [odata[i + j] for j in range(window_size)]
                y1 = np.mat(y) * a0
                y1 = float(y1)
                ndata.append(y1)
            return ndata

        def SG(data_x, window_size=15, rank=2):

            n = data_x.shape[0]  # 样本数量
            data = np.zeros_like(np.array(data_x))

            for i in range(n):
                data[i, :] = data_x.iloc[i, :]

            ans = []
            for i in range(data.shape[0]):
                ans.append(sg(list(data[i, :]), window_size, rank))
            return pd.DataFrame(np.array(ans), columns=data_x.columns)

        # --------------------------------------SG end--------------------------------------

        # ----------------------------------------FD----------------------------------------
        def FD(data_x):
            """
            一阶差分
            """
            temp2 = data_x.diff(axis=1)
            temp3 = temp2.values
            return pd.DataFrame(np.delete(temp3, 0, axis=1), columns=data_x.columns[1:])

        # --------------------------------------FD end--------------------------------------

        # ----------------------------------------SD----------------------------------------
        def SD(data_x):
            """
            二阶差分
            """
            temp2 = data_x.diff(axis=1)
            temp3 = np.delete(temp2.values, 0, axis=1)
            temp4 = (pd.DataFrame(temp3)).diff(axis=1)
            spec_D2 = np.delete(temp4.values, 0, axis=1)
            return pd.DataFrame(spec_D2, columns=data_x.columns[2:])

        # --------------------------------------SD end--------------------------------------

        # ---------------------------------------SNV----------------------------------------
        def SNV(data):
            """
            标准正态变换
            """
            n = data.shape[0]  # 样本数量
            data_x = np.zeros_like(np.array(data))
            for i in range(n):
                data_x[i, :] = data.iloc[i, :]

            n, p = data_x.shape
            snv_x = np.ones((n, p))
            data_std = np.std(data_x, axis=1)
            data_average = np.mean(data_x, axis=1)

            for i in range(n):
                for j in range(p):
                    snv_x[i][j] = (data_x[i][j] - data_average[i]) / data_std[i]

            return pd.DataFrame(snv_x, columns=data.columns)

        # -------------------------------------SNV end--------------------------------------

        # ---------------------------------------MSC----------------------------------------
        def MSC(data):
            """
            多元散射校正
            """
            n = data.shape[0]  # 样本数量
            data_x = np.zeros_like(np.array(data))

            for i in range(n):
                data_x[i, :] = data.iloc[i, :]

            # data_x = np.array(data)
            # print(data_x.shape)
            # print(data)
            mean = np.mean(data_x, axis=0)
            n, p = data_x.shape
            msc_x = np.ones((n, p))
            for i in range(n):
                y = data_x[i, :]
                lin = LinearRegression()
                lin.fit(mean.reshape(-1, 1), y.reshape(-1, 1))
                k = lin.coef_
                b = lin.intercept_
                msc_x[i, :] = (y - b) / k
            return pd.DataFrame(msc_x, columns=data.columns)

        # -------------------------------------MSC end--------------------------------------

        # ----------------------------------------MC----------------------------------------
        def MC(data):
            """
            均值中心化
            """
            np.mean(data, axis=0)
            return pd.DataFrame(data - np.mean(data, axis=0))

        # --------------------------------------MC end--------------------------------------

        # ----------------------------------------LG----------------------------------------
        def LG(data):
            """
            对数变换
            """
            n = data.shape[0]
            data_x = np.zeros_like(np.array(data))
            for i in range(n):
                data_x[i, :] = data.iloc[i, :]

            n, p = data_x.shape
            LG_x = np.ones((n, p))

            for i in range(n):
                for j in range(p):
                    LG_x[i][j] = (math.log(1 / data_x[i][j], 10))
            return pd.DataFrame(LG_x, columns=data.columns)

        # --------------------------------------LG end--------------------------------------

        print("[*] 当前预测数据的形状：{}".format(data.shape))
        print("[*] 数据样例：")
        print(data)

        if ("+" in way):
            step = way.split("+")
            if (len(step) == 2):
                data_mid = eval(step[0])(data)
                data1 = eval(step[1])(data_mid)
            elif (len(step) == 3):
                data_mid = eval(step[0])(data)
                data_after = eval(step[1])(data_mid)
                data1 = eval(step[2])(data_after)
            else:
                raise Exception('[!] 预处理组合不合理，超出最大组合范围')
        else:
            data1 = eval(way)(data)
        return data1

    def draw(self, data, way):
        data_after = self.pretreatment_handler(data, way)
        plot = draw_pic_way(data_after, way)
        return plot

    def check(self):
        pre_way, model_name = self.assessment_handler()
        return pre_way, model_name

if __name__ == '__main__':
    check = NirspyCheck('default')
    pre_way, model_name = check.check()
    data = pd.read_csv(r'E:\大学生创新创业\demo\data.csv')
    plot = check.draw(data, pre_way)
    print(plot)
