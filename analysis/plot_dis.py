import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置字体和标签格式
TITLE_FONT = {'family':'Arial', 'size':16, 'fontweight':'bold'}
LABEL_FONT = {'family':'Arial', 'size':12, 'fontweight':'bold'}
LEGEND_FONT = {'family':'Arial', 'size': 10, 'weight': 'bold'}

# 绘制折线图的简化函数
def plot_curve(ax, df, title, x_column='Frame', y_columns=None, colors=None, xlabel='time (ns)', ylabel='Distance from Ser592-CB to ligand (Å)', x_true=500, x_min=0, x_max=1000, y_min=0, y_max=None):
    if y_columns is None:
        y_columns = df.columns[1:]  # 默认绘制除X轴外的所有列
    
    if colors is None:
        colors = ['green', 'purple', 'blue', 'orange', 'orange', 'purple', 'red'][:len(y_columns)]  # 默认颜色

    # 绘制每一列的折线
    for i, y_column in enumerate(y_columns):
        ax.plot(df[x_column]/(len(df)/x_true), df[y_column], color=colors[i], linewidth=1, label=y_column)
    ax.axhline(y=12, color='red', linestyle='--', linewidth=1, label='12Å cutoff')
    # 设置图例、标签、标题等
    ax.set_xlabel(xlabel, fontdict=LABEL_FONT)
    ax.set_ylabel(ylabel, fontdict=LABEL_FONT)
    ax.set_xlim([x_min, x_true])
    if y_max:
        ax.set_ylim([y_min, x_true])
    
    ax.legend(loc='upper left', prop=LEGEND_FONT)
    ax.set_title(title, fontdict=TITLE_FONT)



df = pd.read_csv('total_dis.csv',sep='\t')
print(df.mean())
count_less_than_12 = (df < 12).sum()
print(count_less_than_12)
fig, ax = plt.subplots(figsize=(8, 6))
plot_curve(ax, df, title="")
plt.savefig('dis.png')
