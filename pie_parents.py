# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:27:00 2023

@author: DengAoQian
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'G:\\11.23noddi\\step3\\other_clinical\\input.xlsx'
data = pd.read_excel(file_path)

# Filter data for subtype 0 and 1
subtype0_data = data[data['subtype'] == 0]
subtype1_data = data[data['subtype'] == 1]

# Calculate the counts of now_suicide3 for each subtype
subtype0_now_suicide3_counts = subtype0_data['parents'].value_counts()
subtype1_now_suicide3_counts = subtype1_data['parents'].value_counts()

# Define color themes for subtypes
colors_subtype0_lighter = ['#b3cde0', '#cce2e8']  # Light blue-grey theme
colors_subtype1 = ['#f7cac9', '#f9e2e2']  # Light red theme

# Creating pie charts with the adjusted color theme and labels
plt.rcParams.update({'font.size': 25})  # Adjusting the base font size
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

# Labels for subtype 0 and subtype 1
subtype0_counts = [f"No direct family history (n={subtype0_now_suicide3_counts[2]})", 
                   f"Direct family history (n={subtype0_now_suicide3_counts[1]})"]
subtype1_counts = [f"No direct family history (n={subtype1_now_suicide3_counts[2]})", 
                   f"Direct family history (n={subtype1_now_suicide3_counts[1]})"]

# Pie chart for subtype 0
axs[0].pie(subtype0_now_suicide3_counts, labels=subtype0_counts, autopct='%1.1f%%', startangle=140, colors=colors_subtype0_lighter, textprops={'fontsize': 19})
axs[0].set_title('Frontal-led', fontsize=25)

# Pie chart for subtype 1
axs[1].pie(subtype1_now_suicide3_counts, labels=subtype1_counts, autopct='%1.1f%%', startangle=140, colors=colors_subtype1, textprops={'fontsize': 19})
axs[1].set_title('Hippocampus-led', fontsize=25)

plt.tight_layout()

# Saving the figures in PDF and PNG format
output_path_pdf = 'G:\\11.23noddi\\step3\\other_clinical\\family history.pdf'
output_path_png = 'G:\\11.23noddi\\step3\\other_clinical\\family history.png'
plt.savefig(output_path_pdf, format='pdf', dpi=600,bbox_inches='tight')
plt.savefig(output_path_png, format='png', dpi=600, bbox_inches='tight')

plt.show()