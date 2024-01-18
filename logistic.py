# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:56:03 2023

@author: DengAoQian
"""

import pandas as pd
from statsmodels.formula.api import logit
import numpy as np

# 加载数据
file_path = 'G:\\11.23noddi\\step3\\other_clinical\\input1.xlsx'  # 请替换为您的文件路径
df = pd.read_excel(file_path)

# 调整 'nowsuicide3' 变量从 (1, 2) 到 (0, 1)
df['parents'] = df['parents'] - 1

# 运行逻辑回归模型，包含 'parents' 变量
model = logit("parents ~ subtype + age + sex", data=df).fit()

# 将模型摘要转换为字符串
model_summary_str = model.summary().as_text()

# 计算Odds比
odds_ratios = np.exp(model.params)
odds_ratios_str = odds_ratios.to_string()

# 将模型摘要和Odds比一起保存到文本文件中
full_output = model_summary_str + '\n\nOdds Ratios:\n' + odds_ratios_str

# 准备保存摘要的文件路径
output_file_path = 'G:\\11.23noddi\\step3\\other_clinical\\Table\\logistic_regression_parents.txt'  # 请替换为您的文件路径

# 将摘要保存到文本文件
with open(output_file_path, 'w') as file:
    file.write(full_output)
