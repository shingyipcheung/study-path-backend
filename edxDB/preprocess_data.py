import pandas as pd
import numpy as np
from edxDB.course_structure_parser import truncate_by_special_char
from edxDB.constants import PROBLEM_WEIGHT, CONCEPT_EDGES, GRADE_FILE


def minify_problem_records():
    df = pd.read_table(GRADE_FILE)
    # filter module_type which is problem
    df = df[df["module_type"] == "problem"]
    # filter only needed columns
    df = df[["student_id", "module_id", "grade", "max_grade"]]  # state
    # cut the last hash id
    df['module_id'] = df['module_id'].map(truncate_by_special_char)
    df.rename(columns={"module_id": "problem_id"}, inplace=True)
    df.to_pickle("problem_records.pkl")
    return df


def weight_dataframe():
    weight_list = []
    for concept, problems in PROBLEM_WEIGHT.items():
        for problem_id, weight in problems.items():
            weight_list.append({"concept": concept, "problem_id": problem_id, "weight": weight})

    return pd.DataFrame(weight_list)


def generate_concept_grade():
    problem_df = minify_problem_records()
    weight_df = weight_dataframe()
    # filter grade only >= 0
    problem_df = problem_df[problem_df["grade"] >= 0]
    # inner join
    df = pd.merge(problem_df, weight_df, on='problem_id', how='inner')
    # concept score for one question # normalize using the max grade of the question
    df["weighted_grade"] = df["grade"] * df["weight"] / df["max_grade"]
    # sum all concept score for all questions
    df = df.groupby(["student_id", "concept"]).agg({"weighted_grade": "sum"})
    # reshape to concepts columns
    df = df.unstack(fill_value=np.nan)
    # drop column level "sum"
    df.columns = df.columns.droplevel(level=0)
    # min-max normalization
    df = (df - df.min()) / (df.max() - df.min())
    df = df.round(2)
    # replace nan with none
    df = df.where((pd.notnull(df)), None)
    df.to_pickle("student_concept_grade.pkl")
    print(df)
    return df


def risk_ratio(df: pd.DataFrame, mean, left: str, right: str):
    left_fail = df[df[left] < mean[left]].index
    left_pass = df[df[left] >= mean[left]].index
    right_fail = df[df[right] < mean[right]].index
    right_pass = df[df[right] >= mean[right]].index

    """
    https://en.wikipedia.org/wiki/Relative_risk
          right
           - +
    left -|a|b|
         +|c|d|
    """
    # get the sizes of sets
    a = left_fail.intersection(right_fail).shape[0]
    b = left_fail.intersection(right_pass).shape[0]
    c = left_pass.intersection(right_fail).shape[0]
    d = left_pass.intersection(right_pass).shape[0]
    # print('left:', left, 'right:', right)
    # print(len(left_fail), len(left_pass), len(right_fail), len(right_pass))
    # print('a:', a, 'b:', b, 'c:', c, 'd:', d)
    # print("==============")
    return (a / (a + b)) / (c / (c + d))


def generate_risk_ratio():
    ratio_list = []
    df = generate_concept_grade()
    # df.replace(0, np.nan
    mean = df.mean()
    print(mean)
    mean.to_pickle("concept_score_mean.pkl")
    for u, v_list in CONCEPT_EDGES.items():
        for v in v_list:
            ratio = {"source": u, "target": v, "value": risk_ratio(df, mean, u, v)}
            ratio_list.append(ratio)
    ratio_df = pd.DataFrame(ratio_list)
    ratio_df.to_pickle("risk_ratio.pkl")
    return ratio_df


def main():
    df = generate_risk_ratio()
    print(df)


if __name__ == '__main__':
    main()
