# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:58:15 2023

@author: DengAoQian
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 加载 Excel 文件
file_path = 'G:\\11.23noddi\\step3\\other_clinical\\cognitive_figure.xlsx'
data = pd.read_excel(file_path)

# 处理缺失值
data_clean = data.dropna(subset=['executive function', 'age', 'sex', 'education', 'subtype'])

# 重命名列以去除空格
data_clean.rename(columns={'executive function': 'executive_function'}, inplace=True)

# 构建线性模型
model = ols('executive_function ~ C(subtype) + age + C(sex) + education', data=data_clean).fit()

# 获取模型摘要
model_summary = model.summary()

# 打印模型摘要
print(model_summary)

# 保存模型摘要到文件
output_file_path = 'G:\\11.23noddi\\step3\\other_clinical\\Table\\model_summary.txt'
with open(output_file_path, 'w') as f:
    f.write(model_summary.as_text())
