# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 19:33:33 2023

@author: DengAoQian
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置文件路径
excel_file_path = 'G:\\11.23noddi\\step3\\other_clinical\\cognitive_figure.xlsx'
output_image_path = 'G:\\11.23noddi\\step3\\other_clinical\\violin_plot_stage.png'
output_pdf_path = 'G:\\11.23noddi\\step3\\other_clinical\\violin_plot_stage1.pdf'
# 读取Excel文件
data = pd.read_excel(excel_file_path)

# 清理数据：去除包含空值的行
data_cleaned = data.dropna(subset=['executive function', 'attention', 'processing', 'memory'])

# 添加平均值列作为整体认知功能
data_cleaned['average'] = data_cleaned[['executive function', 'attention', 'processing', 'memory']].mean(axis=1)

# 将数据转换为长格式以便于绘图
melted_data = pd.melt(data_cleaned, id_vars=['stage'], value_vars=['executive function', 'attention', 'processing', 'memory', 'average'], var_name='Variable', value_name='Score')

# 定义颜色
violin_colors = ['#B4D9FD', '#FCC8E1']  # 小提琴图颜色
strip_colors = ['#75BAFD', '#FD96C7']    # 数据点颜色

# 绘制小提琴图
plt.figure(figsize=(14, 8))
sns.violinplot(x='Variable', y='Score', hue='stage', data=melted_data, split=True, palette=violin_colors, inner=None)
sns.stripplot(x='Variable', y='Score', hue='stage', data=melted_data, dodge=True, edgecolor='gray', palette=strip_colors, size=4)

# 调整图例
handles, labels = plt.gca().get_legend_handles_labels()
half = len(handles) // 2
plt.legend(handles[:half], ['Neurite Integrity', 'Neurite Anomalies'], loc='upper right', frameon=False, prop={'size': 20})

plt.title("Cognitive Functions in Two Stages")
plt.xlabel('Cognitive Function')
plt.ylabel('Z Score')

plt.tight_layout()

# 保存图像
plt.savefig(output_image_path, format='png', dpi=600,bbox_inches='tight')
plt.savefig(output_pdf_path, format='pdf', dpi=600,bbox_inches='tight')

# 如果需要在屏幕上显示图像
# plt.show()



