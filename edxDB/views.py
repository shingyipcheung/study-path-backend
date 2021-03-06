from django.http import JsonResponse, HttpResponse
import pandas as pd
from .constants import *
from .df_loader import load_df, local_path
import os
from functools import lru_cache

from .path import generate_paths


def videos(request, concept):
    return JsonResponse(VIDEO_DICT[concept], safe=False)


def graph(request):
    df = load_df("risk_ratio.pkl")
    return JsonResponse(df.to_dict(orient='records'), safe=False)


def concepts(request):
    return JsonResponse(CONCEPTS, safe=False)


def means(request):
    df = load_df("concept_score_mean.pkl")
    return JsonResponse(df.round(2).to_dict(), safe=False)


def problem(request, problem_id):
    df = load_df("problem_records.pkl")
    problem_df = df[df["problem_id"] == problem_id]
    sorted_grade = problem_df[["student_id", "grade"]].sort_values(by=["grade"])
    return JsonResponse(sorted_grade.to_dict(orient="list"), safe=False)


@lru_cache()
def load_xml(problem_id):
    return open(local_path(os.path.join("data", "problem", problem_id + '.xml')), encoding='utf8').read()


@lru_cache()
def is_mc_problem(problem_id):
    if "<multiple" in load_xml(problem_id):
        print(problem_id, "is", "a mc question")
        return True
    return False


def problems(request, concept):
    return JsonResponse(list(filter(is_mc_problem, PROBLEM_WEIGHT[concept].keys())), safe=False)


def problem_html(request, problem_id):
    return HttpResponse(load_xml(problem_id))


def concept_score(request, student_id):
    df = load_df("student_concept_grade.pkl")
    student_id = int(student_id)
    student = df.loc[student_id].to_dict()
    student["student_id"] = student_id
    return JsonResponse(student, safe=False)


def concept_score_all(request):
    df = load_df("student_concept_grade.pkl")
    return JsonResponse(df.reset_index().to_dict(orient='records'), safe=False)


def recommendation(request, student_id):
    df = load_df("student_concept_grade.pkl")
    student_id = int(student_id)
    student = df.loc[student_id]
    student = student.rename("grade")
    mean = load_df("concept_score_mean.pkl")
    mean = mean.rename("mean")
    df = pd.concat([student, mean], axis=1)

    # https://bootstrap-vue.js.org/docs/components/table
    def row_variant(row):
        if row["grade"] is not None and row["grade"] >= row["mean"]:
            # path.remove(row.name)
            return "success"
        return "danger"

    df["_rowVariant"] = df.apply(row_variant, axis=1)
    df = df.round(2)

    df.index.rename('Learning Object', inplace=True)
    df.rename(columns={'grade': 'Score', 'mean': 'Avg. Score'}, inplace=True)
    df = df.round(2)
    return JsonResponse({
        "table": df.reset_index().to_dict(orient='records'),
        "paths": generate_paths(student_id)
    }, safe=False)
