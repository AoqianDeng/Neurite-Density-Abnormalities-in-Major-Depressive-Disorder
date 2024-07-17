# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:16:17 2023

@author: DengAoQian
"""
import matplotlib.pyplot as plt
import pandas as pd

# Load your data
file_path = 'G:\\11.23noddi\\step3\\TMS\\TMS.xlsx'
data = pd.read_excel(file_path)

# Prepare data for plotting
subtype0_data = data[data['stage'] == 0]
subtype1_data = data[data['stage'] == 1]

time_points = ['HAMDbaseline', '1day', '5day', '2week', '4week', '8week', '6month']
clinical_time_points = ['Baseline', 'Day 1', 'Day 5', 'Week 2', 'Week 4', 'Week 8', 'Month 6']
subtype0_means = subtype0_data[time_points].mean()
subtype1_means = subtype1_data[time_points].mean()
subtype0_sems = subtype0_data[time_points].sem()
subtype1_sems = subtype1_data[time_points].sem()

# Colors
professional_colors = {'Neurite Integrity': '#377eb8', 'Neurite Anomalies': '#d73027'}

# Create the plot with adjusted figure size for better fit
fig, ax = plt.subplots(figsize=(10, 8))  # Adjusted for a better fit in the final files

ax.errorbar(clinical_time_points, subtype0_means, yerr=subtype0_sems, fmt='-o', 
            color=professional_colors['Neurite Integrity'], label='Frontal-led', 
            capsize=3, capthick=1, elinewidth=2, markeredgewidth=2)
ax.errorbar(clinical_time_points, subtype1_means, yerr=subtype1_sems, fmt='-o', 
            color=professional_colors['Neurite Anomalies'], label='Hippocampus-led', 
            capsize=3, capthick=1, elinewidth=2, markeredgewidth=2)

# Title and labels with adjusted title position
ax.set_title('HAM-D Score of Two MDD Subtypes Across the TMS Treatment Trial', fontsize=16, pad=20)
ax.set_xlabel('Time Points', fontsize=14)
ax.set_ylabel('HAM-D Score', fontsize=14)
ax.set_xticks(range(len(clinical_time_points)))
ax.set_xticklabels(clinical_time_points, rotation=45)
ax.legend(loc='upper right', fontsize=12)
ax.set_ylim(0, 25)

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
output_folder = 'G:\\11.23noddi\\step3\\TMS\\'
pdf_file_path = output_folder + 'TMS_plot_stage.pdf'
png_file_path = output_folder + 'TMS_plot_stage.png'
fig.savefig(pdf_file_path, format='pdf', dpi=300, bbox_inches='tight')
fig.savefig(png_file_path, format='png', dpi=300, bbox_inches='tight')

plt.show()
