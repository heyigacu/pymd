import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 设置 Seaborn 风格
sns.set(style="whitegrid")

# 创建原始数据
data = {
    'Inhibitor': ['Fulvestrant', 'Meropenem', 'Paliperidone', 'Isavuconazonium'],
    'IC50 (μmol)': [66.33, 45.81, 48.87, 6.60],
    'GaMD MMPB/SA (kcal/mol)': [-47.80, -37.26, -37.73, -42.60],
    'Number of contacts': [1, 4, 1, 40],
    'Residence time (ns)': [0.6, 37.6, 1.1, 500],
    'Mean distance to Ser592 (Å)': [43.81, 31.54, 33.1, 5.19]
}

df = pd.DataFrame(data)


# 处理 'Number of contacts' 列
df['Number of contacts'] = pd.to_numeric(df['Number of contacts'], errors='coerce')

# 可视化回归曲线
x = 'IC50 (μmol)'
y_variables = ['GaMD MMPB/SA (kcal/mol)', 'Number of contacts', 'Residence time (ns)', 'Mean distance to Ser592 (Å)']

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

for i, y in enumerate(y_variables):
    sns.regplot(x=x, y=y, data=df, ax=axes[i])
    axes[i].set_title(f'{y} vs IC$_{{50}}$ (μmol)', fontsize=14)  # 设置标题，其中 IC50 的 50 为下标
    axes[i].set_xlabel('IC$_{50}$ (μmol)', fontsize=12)  # 设置 x 轴标签
    axes[i].set_ylabel(y, fontsize=12)  # 设置 y 轴标签

plt.tight_layout()

plt.savefig('relation.png')
plt.show()