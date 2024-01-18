

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os
from scipy import stats
import scipy
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
import matplotlib.pyplot as plt

# Load the data
file_path = 'G:\\11.23noddi\\step3\\TMS\\TMS1.xlsx'
data = pd.read_excel(file_path)

# Preparing the data by dropping rows with missing values
data_clean = data.dropna(subset=['HAMD', 'sex', 'age', 'time', 'stage'])

# Calculating Variance Inflation Factor (VIF) for each explanatory variable to check for multicollinearity
X = data_clean[['time', 'stage', 'sex', 'age']]
X = sm.add_constant(X)
vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns

# Building the mixed effects model
model = smf.mixedlm("HAMD ~ time * stage + sex + age", data_clean, groups=data_clean['id'])
model_fit = model.fit()

# Displaying the summary of the model
print(model_fit.summary())

# Fit the reduced model without the interaction term
reduced_model = smf.mixedlm("HAMD ~ time + stage + sex + age", data_clean, groups=data_clean['id'])
reduced_model_fit = reduced_model.fit()

# Calculate the number of parameters for each model
params_full = len(model_fit.params)
params_reduced = len(reduced_model_fit.params)

# Calculate the degrees of freedom for the likelihood ratio test
lrt_df = params_full - params_reduced

# Calculate the likelihood ratio test statistic
lrt_statistic = -2 * (reduced_model_fit.llf - model_fit.llf)
lrt_p_value = scipy.stats.chi2.sf(lrt_statistic, lrt_df)

# Print the likelihood ratio test result
print(f"Likelihood Ratio Test Statistic: {lrt_statistic}")
print(f"Degrees of Freedom: {lrt_df}")
print(f"P-value of the LRT: {lrt_p_value}")

# Residual analysis
residuals = model_fit.resid
fitted = model_fit.fittedvalues
# Residual plot for homoscedasticity
plt.scatter(fitted, residuals)
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.title('Residual vs. Fitted')
plt.show()

# QQ plot for normality
sm.qqplot(residuals, line='45')
plt.title('Normal Q-Q')
plt.show()

# Breusch-Pagan test for homoscedasticity
bp_test = het_breuschpagan(residuals, model_fit.model.exog)
print('Breusch-Pagan test results:', bp_test)

# Durbin-Watson test for autocorrelation
dw_test = durbin_watson(residuals)
print('Durbin-Watson statistic:', dw_test)

# Save the model summary, VIF, and additional analyses to a file
output_dir = 'G:\\11.23noddi\\step3\\TMS'
output_file = 'output_parameters1.txt'

# Check if the directory exists, if not create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir, output_file), 'w') as file:
    file.write(model_fit.summary().as_text())
    file.write("\nVIF Results:\n")
    file.write(vif.to_string(index=False))
    file.write(f"\nLikelihood Ratio Test Statistic: {lrt_statistic}\n")
    file.write(f"Degrees of Freedom: {lrt_df}\n")
    file.write(f"P-value of the LRT: {lrt_p_value}\n")
    file.write(f"Breusch-Pagan test: {bp_test}\n")
    file.write(f"Durbin-Watson statistic: {dw_test}\n")

print(f"Model results and additional analyses saved to {os.path.join(output_dir, output_file)}")

