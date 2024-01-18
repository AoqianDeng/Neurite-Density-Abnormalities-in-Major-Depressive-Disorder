# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:26:44 2023

@author: DengAoQian
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# 读取数据
file_path = 'G:/11.23noddi/2m/stage.xlsx'
data = pd.read_excel(file_path)

# 重命名 subtype 类别
data_renamed = data.copy()
data_renamed['subtype'] = data['subtype'].map({0: 'frontal-led', 1: 'hippocampus-led'})
data_renamed['2m_subtype'] = data['2m_subtype'].map({0: 'frontal-led', 1: '   hippocampus-led'})

# 准备数据
confusion_matrix_data = pd.crosstab(data_renamed['subtype'], data_renamed['2m_subtype'])

# 自定义颜色映射
cmap_custom = LinearSegmentedColormap.from_list("custom_cmap", ['#F5EDEC', '#D3563F'])

# 增大字体大小
plt.rcParams.update({'font.size': 20})

# 绘制热图
plt.figure(figsize=(10, 7))
sns.heatmap(confusion_matrix_data, annot=True, cmap=cmap_custom, fmt='g')
plt.title("Subtype Trends from Baseline to Week 8", fontsize=20)
plt.xlabel("Week 8 Subtype", fontsize=20)
plt.ylabel("Baseline Subtype", fontsize=20)

# 保存图片
output_path = 'G:/11.23noddi/2m/subtype_trends.png'
plt.savefig(output_path,format='png', dpi=600, bbox_inches='tight')

# 显示图片
plt.show()

# 重置字体大小
plt.rcParams.update({'font.size': 20})
