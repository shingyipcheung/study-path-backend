import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency


mapping = {
    "Strongly Disagree": -3,
    "Disagree": -2,
    "Slightly Disagree": -1,
    "Neutral": 0,
    "Slightly Agree": 1,
    "Agree": 2,
    "Strongly Agree": 3,
}


if __name__ == "__main__":
    df = pd.read_csv('Questionnaire on the Study Plan Tool.csv')
    # remove columns containing comments or null response
    df.dropna(axis='columns', inplace=True)
    # replace the string to number by the mapping
    df.replace(mapping, inplace=True)
    columns = df.columns.get_values()
    # for i in columns[1:]:
    #     print(i)
    #     print("mean", df[i].mean())
    #     print("std ", df[i].std())
    #     print("frequency")
    #     print(df[i].value_counts().sort_index())

    result = []
    # start from 1: index 0 is timestamp
    for i in columns[1:-2]:
        result.append([])
        # last two columns are overall ratings
        for j in columns[-2:]:
            # calculate the p value
            chi2, p, dof, ex = chi2_contingency(pd.crosstab(df[i], df[j]).values)
            result[-1].append(p)
        print(i)
        print(result[-1])
        print("=====================")
    result = np.array(result)
    np.set_printoptions(suppress=True)
    print(result)
    print(result < 0.05)
