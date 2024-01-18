import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the data from the specified Excel file
icc_data = pd.read_excel('G:\\11.23noddi\\test-retest\\cc\\icc.xlsx', header=None)

# Reshape the loaded data into a 9x10 matrix
icc_matrix = icc_data.values.reshape(9, 10)

# Set the row labels as specified
row_labels = [f'{i}-{i+9}' for i in range(1, 82, 10)]

# Create the heatmap with high resolution. Set the DPI value higher, e.g., 300 for high-quality output.
plt.figure(figsize=(10, 8), dpi=300)
ax = sns.heatmap(icc_matrix, annot=True, fmt=".2f", cmap="copper", 
                 annot_kws={"size": 12},  # Increase annotation font size
                 cbar_kws={'ticks': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]},  # Specify colorbar ticks
                 vmin=0.5, vmax=1.0)
plt.yticks(np.arange(9) + 0.5, row_labels, rotation=0, fontsize=12)  # Increase y-axis label font size
plt.xticks([])  # Remove the column tick labels

# Adjust colorbar tick label size
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)

# Save the heatmap to the specified path
plt.savefig('G:\\11.23noddi\\test-retest\\cc\\icc_heatmap.png', bbox_inches='tight', dpi=600)

# Optionally, display the plot
plt.show()

