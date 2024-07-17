# -*- coding: utf-8 -*-
"""

Created on Wed Dec 27 17:13:51 2023

@author: DengAoQian
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression  # 导入线性回归模型

# 加载数据集
df_hc1 = pd.read_excel('G:\\11.23noddi\\normalize_new_step2\\dataset1.xlsx')
df_hc2 = pd.read_excel('G:\\11.23noddi\\normalize_new_step2\\dataset2.xlsx')
df_mdd = pd.read_excel('G:\\11.23noddi\\normalize_new_step2\\MDD.xlsx')

# 定义GMV列和特征列
gmv_columns = df_hc1.columns[0:16]
features = ['age', 'sex']

# 标准化MSE评估函数
def smse(y_true, y_pred):
    mse = np.mean((y_true - y_pred) ** 2)
    variance = np.var(y_true, ddof=1)  # 使用ddof=1来获取无偏估计的方差
    return mse / variance

def train_and_evaluate_model(X, y):
    kf = KFold(n_splits=10, shuffle=True, random_state=40)
    smse_scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model = LinearRegression().fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = smse(y_test, y_pred)
        smse_scores.append(score)

    return np.mean(smse_scores), model

# 对每个GMV列进行模型训练和评估（使用df_hc1）
best_models = {}
train_smses = {}

for gmv_col in gmv_columns:
    X = df_hc1[features]
    y = df_hc1[gmv_col]

    avg_smse, best_model = train_and_evaluate_model(X, y)
    best_models[gmv_col] = best_model
    train_smses[gmv_col] = avg_smse

# 输出每个GMV的平均训练SMSE（使用df_hc1）
for gmv_col, smse_value in train_smses.items():
    print(f"Average training SMSE for {gmv_col} using df_hc1: {smse_value}")

# 使用数据集df_hc2进行泛化测试
generalization_smses = {}
X_hc2 = df_hc2[features]
for gmv_col, model in best_models.items():
    y_true = df_hc2[gmv_col]
    y_pred = model.predict(X_hc2)
    score = smse(y_true, y_pred)
    generalization_smses[gmv_col] = score

# 输出泛化测试的SMSE（使用df_hc2）
for gmv_col, smse_score in generalization_smses.items():
    print(f"Generalization SMSE for {gmv_col} using df_hc2: {smse_score}")

# 计算df_hc1数据集中每个GMV列的标准差
std_hc1 = df_hc1[gmv_columns].std()

# 应用最优模型于MDD患者并计算Z值
X_mdd = df_mdd[features]
z_scores = {}
all_predictions = {}

for gmv_col, model in best_models.items():
    y_true = df_mdd[gmv_col]
    y_pred = model.predict(X_mdd)
    z_score = (y_true - y_pred) / std_hc1[gmv_col]
    z_scores[gmv_col] = z_score
    all_predictions[gmv_col] = y_pred.tolist()

# 输出每个MDD受试者的Z值
for gmv_col, z_score in z_scores.items():
    print(f"Z-scores for {gmv_col} using df_mdd: {z_score}")

# 输出所有GMV列的预测值（使用df_mdd）
print("\nPredicted values for each GMV column in MDD patients:")
for gmv_col, predictions in all_predictions.items():
    print(f"{gmv_col}: {predictions}")

# 创建一个新的DataFrame来存储所有GMV列的预测值
predictions_df = pd.DataFrame(all_predictions)
predictions_df.index = df_mdd.index  # 使用MDD数据集的索引作为行索引

# 保存预测值到Excel文件
predictions_df.to_excel('G:\\11.23noddi\\normalize_new_step2\\z_predict_MDD.xlsx')

# 创建一个新的DataFrame来存储Z值
z_scores_df = pd.DataFrame(z_scores)
z_scores_df.index = df_mdd.index  # 使用MDD数据集的索引作为行索引

# 保存Z值到Excel文件
z_scores_df.to_excel('G:\\11.23noddi\\normalize_new_step2\\MDD_Z_sustain_input.xlsx')

print("Predicted values and Z-scores have been saved to Excel.")

# 对df_hc2中的每个GMV列进行模型训练和评估
best_models2 = {}
train_smses2 = {}

for gmv_col in gmv_columns:
    X2 = df_hc2[features]
    y2 = df_hc2[gmv_col]

    avg_smse2, best_model2 = train_and_evaluate_model(X2, y2)
    best_models2[gmv_col] = best_model2
    train_smses2[gmv_col] = avg_smse2

# 输出df_hc2训练模型的平均训练SMSE
for gmv_col, smse in train_smses2.items():
    print(f"Average training SMSE for {gmv_col} using df_hc2: {smse}")

# 创建一个空的DataFrame以存储SMSE结果
rmse_results = pd.DataFrame()
rmse_results['GMV_Column'] = gmv_columns
rmse_results['HC1_SMSE'] = rmse_results['GMV_Column'].map(train_smses)
rmse_results['Generalization_SMSE'] = rmse_results['GMV_Column'].map(generalization_smses)
rmse_results['HC2_SMSE'] = rmse_results['GMV_Column'].map(train_smses2)

# 保存到Excel文件
rmse_results.to_excel('G:\\11.23noddi\\normalize_new_step2\\SMSE1.xlsx', index=False)

print("SMSE results saved to Excel.")
