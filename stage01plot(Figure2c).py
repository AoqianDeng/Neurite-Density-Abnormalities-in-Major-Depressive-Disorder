# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 20:41:11 2023

@author: DengAoQian
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load your data
file_path = 'G:\\11.23noddi\\step3\\antidepressant\\MDDnew.xlsx'
data = pd.read_excel(file_path)

# Prepare data for plotting
stage0_data = data[data['stage'] == 0]
stage1_data = data[data['stage'] == 1]

# Define time points and calculate means and standard errors (SEMs) for plotting
time_points = ['HAMDbaseline', '2week', '4week', '8week', '6month']
clinical_time_points = ['Baseline', 'Week 2', 'Week 4', 'Week 8', 'Month 6']
stage0_means = stage0_data[time_points].mean()
stage1_means = stage1_data[time_points].mean()
stage0_sems = stage0_data[time_points].sem()
stage1_sems = stage1_data[time_points].sem()

# Define the color scheme
professional_colors = {'Stage 0': '#38349F', 'Stage 1': '#AE3238'}

# Translate the title to English
title_english = "HAM-D Scores During Antidepressant Treatment"

# Create the plot with updated legend and title
fig, ax = plt.subplots(figsize=(10, 8))

ax.errorbar(clinical_time_points, stage0_means, yerr=stage0_sems, fmt='-o', 
            color=professional_colors['Stage 0'], label='Neurite Integrity', 
            capsize=3, capthick=1, elinewidth=2, markeredgewidth=2)
ax.errorbar(clinical_time_points, stage1_means, yerr=stage1_sems, fmt='-o', 
            color=professional_colors['Stage 1'], label='Neurite Anomalies', 
            capsize=3, capthick=1, elinewidth=2, markeredgewidth=2)

# Setting the updated title and labels
ax.set_title(title_english, fontsize=28, pad=20)
ax.set_xlabel('Time Points', fontsize=28)
ax.set_ylabel('HAM-D Score', fontsize=25)
ax.set_xticks(range(len(clinical_time_points)))
ax.set_xticklabels(clinical_time_points, rotation=45)
# Increase the size of the x-axis labels
ax.set_xticklabels(clinical_time_points, rotation=45, fontsize=20)  # Adjusted fontsize here
ax.tick_params(axis='y', labelsize=20)  # 调整纵坐标刻度的字体大小
ax.legend(loc='upper right', fontsize=20)
ax.set_ylim(0, max(stage0_means.max(), stage1_means.max()) + 5)

# Aesthetics
ax.set_facecolor('white')
ax.grid(axis='y', color='grey', linestyle='-', linewidth=0.7, alpha=0.7)
ax.yaxis.grid(True)
ax.xaxis.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tight layout for making sure all plot elements fit within the figure area
fig.tight_layout()

# Save the plot as high-resolution PDF and PNG files
output_folder = 'G:\\11.23noddi\\step3\\antidepressant\\'
pdf_file_path = output_folder + 'MDDstage_plot.pdf'
png_file_path = output_folder + 'MDDstage_plot.png'
fig.savefig(pdf_file_path, format='pdf', dpi=600, bbox_inches='tight')
fig.savefig(png_file_path, format='png', dpi=600, bbox_inches='tight')

plt.show()
