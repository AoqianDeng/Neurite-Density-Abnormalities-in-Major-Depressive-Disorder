# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 15:47:04 2025

@author: DengAoQian
"""

# -*- coding: utf-8 -*-
"""
Plot HAMD trajectories — unified style (2023-11-28 preset)
"""
import pandas as pd
import matplotlib.pyplot as plt

# ───────────────────────────────────── 1. 读取数据
file_path = r'G:\11.23noddi\step3\antidepressant\MDDnew.xlsx'
data = pd.read_excel(file_path)

# ───────────────────────────────────── 2. 准备绘图数据
stage0 = data[data['stage'] == 0]
stage1 = data[data['stage'] == 1]

time_cols  = ['HAMDbaseline', '2week', '4week', '8week', '6month']
x_labels   = ['Baseline', 'Week 2', 'Week 4', 'Month 2', 'Month 6']

mean0 = stage0[time_cols].mean()
mean1 = stage1[time_cols].mean()
sem0  = stage0[time_cols].sem()
sem1  = stage1[time_cols].sem()

colors = {'Stage 0': '#38349F', 'Stage 1': '#AE3238'}

# ───────────────────────────────────── 3. 绘图（统一样式）
fig, ax = plt.subplots(figsize=(10, 8))

ax.errorbar(
    x_labels, mean0, yerr=sem0,
    fmt='-o', color=colors['Stage 0'],
    label='Normal NDI',
    capsize=3, capthick=1, elinewidth=3,
    markeredgewidth=2, linewidth=3
)

ax.errorbar(
    x_labels, mean1, yerr=sem1,
    fmt='-o', color=colors['Stage 1'],
    label='Reduced NDI',
    capsize=3, capthick=1, elinewidth=3,
    markeredgewidth=2, linewidth=3
)

# ───────────────────────────────────── 4. 轴标题与刻度
ax.set_title("HAM-D Scores During Antidepressant Treatment", fontsize=28, pad=20)
ax.set_xlabel("Time Points", fontsize=28)
ax.set_ylabel("HAM-D Score", fontsize=25)

ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, rotation=45, fontsize=20)
ax.tick_params(axis='y', labelsize=20)

ax.set_ylim(0, max(mean0.max(), mean1.max()) + 5)
ax.legend(loc='upper right', fontsize=20)

# ───────────────────────────────────── 5. 视觉细节
ax.set_facecolor('white')
ax.grid(axis='y', color='grey', linestyle='-', linewidth=0.7, alpha=0.7)
ax.yaxis.grid(True); ax.xaxis.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()

# ───────────────────────────────────── 6. 保存
out_dir = r'G:\11.23noddi\step3\antidepressant\\'
fig.savefig(out_dir + 'MDDstage_plot.pdf', format='pdf', dpi=600, bbox_inches='tight')
fig.savefig(out_dir + 'MDDstage_plot.png', format='png', dpi=600, bbox_inches='tight')
plt.show()
