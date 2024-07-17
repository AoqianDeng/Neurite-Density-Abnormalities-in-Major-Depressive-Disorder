# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:52:18 2023

@author: DengAoQian
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pandas.plotting import parallel_coordinates

# 设置字体大小
title_fontsize = 20
label_fontsize = 20

# 设置自定义颜色映射
cmap_updated = LinearSegmentedColormap.from_list("custom_cmap", ['#F5EDEC', '#D3563F'])

# 加载数据
file_path = 'G:/11.23noddi/2m/stage.xlsx'
data = pd.read_excel(file_path)

# 提取相关列并重命名
heatmap_data = data[['stage', '2m_stage']]
heatmap_data.columns = ['baseline', 'week 8']

# 绘制热图
plt.figure(figsize=(14, 6))
ax = sns.heatmap(heatmap_data.T, cmap=cmap_updated, cbar_kws={'label': 'Stage'})
plt.title("Baseline and Week 8 Stages of MDD", fontsize=title_fontsize)
plt.xlabel("")
plt.ylabel("")
plt.xticks([], fontsize=label_fontsize)
plt.yticks(fontsize=label_fontsize)

# 保存图片到指定路径
output_path = 'G:/11.23noddi/2m/baseline_week8_stages.png'
plt.savefig(output_path,format='png', dpi=600, bbox_inches='tight')


