import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Line


def line_base(p, q, data) -> Line:
    df_msc = data
    n = df_msc.shape[0]  # 样本数量
    x = [str(float(i)) for i in list(df_msc.columns)]
    spec_msc = np.zeros_like(np.array(df_msc))
    for i in range(n):
        spec_msc[i, :] = data.loc[i, :]

    c = (
        Line()
        .add_xaxis(x)
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例
            # title_opts=opts.TitleOpts(title=None),  # 隐藏标题
            datazoom_opts=[
                opts.DataZoomOpts(xaxis_index=0),
                opts.DataZoomOpts(type_="inside", xaxis_index=0),
            ],
            title_opts=opts.TitleOpts(title="光谱数据图", subtitle="Nirs System",pos_left="center",pos_top="top")
        )

    )

    for i in range(int(p),int(q)):
        c_ = (
            Line()
            .add_xaxis(x)
            .add_yaxis("第{}条光谱数据".format(i),spec_msc[i,:],
                       label_opts=opts.LabelOpts(is_show=False),
                       linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                       is_smooth=True,
                       is_hover_animation=False,
                       )

        )
        c.overlap(c_)
    return c
