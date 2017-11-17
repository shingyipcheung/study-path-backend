from django.http import JsonResponse
import pandas as pd
import os


workpath = os.path.dirname(os.path.abspath(__file__))


def local_path(filename):
    return os.path.join(workpath, filename)


df_pool = {}


def read_df(filename):
    if filename in df_pool:
        return df_pool[filename]
    extension = os.path.splitext(filename)[1][1:]
    df = None
    if extension == "csv":
        df = pd.read_csv(local_path(filename))
    elif extension == "pkl":
        df = pd.read_pickle(local_path(filename))
    df_pool[filename] = df
    return df


def graph(request):
    df = read_df("risk_ratio.pkl")
    return JsonResponse(df.to_dict('records'), safe=False)


def problem(request, problem_id):
    df = read_df("problem_records.pkl")
    problem_df = df[df["problem_id"] == problem_id]
    sorted_grade = problem_df[["student_id", "grade"]].sort_values(by=["grade"])
    return JsonResponse(sorted_grade.to_dict(orient="list"), safe=False)


def concept_score(request, student_id):
    df = read_df("student_concept_grade.pkl")
    student_id = int(student_id)
    student = df.loc[student_id].to_dict()
    student["student_id"] = student_id
    return JsonResponse(student, safe=False)


def concept_score_all(request):
    df = read_df("student_concept_grade.pkl")
    return JsonResponse(df.reset_index().to_dict('records'), safe=False)
