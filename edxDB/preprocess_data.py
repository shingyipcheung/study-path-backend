import pandas as pd
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
    grade_df = minify_problem_records()
    weight_df = weight_dataframe()
    # filter grade only > 0
    grade_df = grade_df[grade_df["grade"] > 0]
    # right outer join
    df = pd.merge(grade_df, weight_df, on='problem_id', how='right')
    # concept score for one question
    df["weighted_grade"] = df["grade"] * df["weight"]
    # sum all concept score for all questions
    df = df.groupby(["student_id", "concept"]).agg({"weighted_grade": "sum"})
    # reshape to concepts columns
    df = df.unstack(fill_value=0)
    # drop column level "sum"
    df.columns = df.columns.droplevel(level=0)
    df.to_pickle("student_concept_grade.pkl")
    return df


def risk_ratio(df: pd.DataFrame, left: str, right: str):
    mean = df.mean()
    left_below = df[df[left] < mean[left]].index
    left_above = df[df[left] >= mean[left]].index
    right_below = df[df[right] < mean[right]].index
    right_above = df[df[right] >= mean[right]].index
    """
    https://en.wikipedia.org/wiki/Relative_risk
          right
           - +
    left -|a|b|
         +|c|d|
    """
    # get the sizes of sets
    a = left_below.intersection(right_below).shape[0]
    b = left_below.intersection(right_above).shape[0]
    c = left_above.intersection(right_below).shape[0]
    d = left_above.intersection(right_above).shape[0]
    return (a / (a + b)) / (c / (c + d))


def generate_risk_ratio():
    ratio_list = []
    df = generate_concept_grade()
    for u, v_list in CONCEPT_EDGES.items():
        for v in v_list:
            ratio_list.append({"source": u, "target": v, "value": risk_ratio(df, u, v)})
    ratio_df = pd.DataFrame(ratio_list)
    ratio_df.to_pickle("risk_ratio.pkl")
    return ratio_df


def main():
    df = generate_risk_ratio()
    print(df)


if __name__ == '__main__':
    main()
