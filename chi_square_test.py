import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact


def chisq_of_df_cols(df, c1, c2):
    ctsum = pd.crosstab(df[c1], df[c2]).values
    return chi2_contingency(ctsum)


mapping = {
    "Strongly Disagree": -3,
    "Disagree": -2,
    "Slightly Disagree": -1,
    "Neutral": 0,
    "Slightly Agree": 1,
    "Agree": 2,
    "Strongly Agree": 3,
}


df = pd.read_csv('Questionnaire on the Study Plan Tool.csv')
df.dropna(axis='columns', inplace=True)
df.replace(mapping, inplace=True)
columns = df.columns.get_values()
for i in columns[1:]:
    print(i)
    print("mean", df[i].mean())
    print("std ", df[i].std())
    print("frequency")
    print(df[i].value_counts().sort_index())

# remove columns containing comments or null response
result = []
for i in columns[1:-2]:
    result.append([])
    for j in columns[-2:]:
        chi2, p, dof, ex = chisq_of_df_cols(df, i, j)
        result[-1].append(p)
        # print(pd.crosstab(df[i] > 0, df[j] > 0))
        # print(fisher_exact(pd.crosstab(df[i] > 0, df[j] > 0)))
    print(i)
    print(result[-1])
    print("=====================")
result = np.array(result)
np.set_printoptions(suppress=True)
print(result)
print(result < 0.05)
