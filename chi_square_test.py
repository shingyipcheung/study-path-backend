import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency


def chisq_of_df_cols(df, c1, c2):
    ctsum = pd.crosstab(df[c1], df[c2]).values
    return chi2_contingency(ctsum, lambda_="log-likelihood")


df = pd.read_csv('Questionnaire on the Study Plan Tool.csv')
result = []
for i in range(1, 12):
    result.append([])
    for j in range(12, 14):
        chi2, p, dof, ex = chisq_of_df_cols(df, df.columns.get_values()[i], df.columns.get_values()[j])
        result[-1].append(p)
result = np.array(result)
print(result)
print(result < 0.05)
