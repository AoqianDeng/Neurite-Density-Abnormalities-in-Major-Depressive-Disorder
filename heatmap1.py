# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:26:59 2023

@author: DengAoQian
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load the data from the file
file_path = 'G:/11.23noddi/step3/brainnet/heatmap2.xlsx'
data = pd.read_excel(file_path, index_col=0)

# Convert the data to negative as per previous context
data_neg = data * -1

# Create a custom color map with white for 0 and #C65B3F for -3
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', ['white', '#C65B3F'], N=256)

# Create a heatmap with specified settings
plt.figure(figsize=(15, 10))  # Adjust the figure size
sns.heatmap(data_neg, cmap=custom_cmap.reversed(), vmin=-3, vmax=0, cbar_kws={'label': 'Scale', 'orientation': 'vertical'})

# Adjust the color bar label size
cbar = plt.gcf().axes[-1]
cbar.set_ylabel('Scale', fontsize=25, weight='bold')
cbar.tick_params(labelsize=25)

# Setting x-ticks and y-ticks with larger font size
xtick_positions = [0, 10, 20, 30]  # Define x-tick positions
plt.xticks(ticks=xtick_positions, labels=[str(pos) for pos in xtick_positions], fontsize=25, rotation=0)
plt.yticks(fontsize=30)

# Setting bold labels for axes with larger font size
plt.xlabel('SuStain stage', fontsize=25)
plt.ylabel('Regions', fontsize=25)

# Limiting x-axis to show only 0-35
plt.xlim(0, 35)

# Adjust layout to make sure y-axis labels are fully displayed
plt.tight_layout()

# Save the plot as a high-resolution PDF and PNG
save_path_pdf = 'G:/11.23noddi/step3/brainnet/heatmap2_custom_color_large_font.pdf'
save_path_png = 'G:/11.23noddi/step3/brainnet/heatmap2_custom_color_large_font.png'
plt.savefig(save_path_pdf, format='pdf', dpi=900)
plt.savefig(save_path_png, format='png', dpi=900)

# Show the plot
plt.show()

