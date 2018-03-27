from django.http import JsonResponse
import pandas as pd
from .constants import PROBLEM_WEIGHT, VIDEO_DICT
from .df_loader import load_df


def videos(request, concept):
    return JsonResponse(VIDEO_DICT[concept], safe=False)


def graph(request):
    df = load_df("risk_ratio.pkl")
    return JsonResponse(df.to_dict(orient='records'), safe=False)


def concepts(request):
    return JsonResponse(list(PROBLEM_WEIGHT.keys()), safe=False)


def means(request):
    df = load_df("concept_score_mean.pkl")
    return JsonResponse(df.round(2).to_dict(), safe=False)


def problem(request, problem_id):
    df = load_df("problem_records.pkl")
    problem_df = df[df["problem_id"] == problem_id]
    sorted_grade = problem_df[["student_id", "grade"]].sort_values(by=["grade"])
    return JsonResponse(sorted_grade.to_dict(orient="list"), safe=False)


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

    path = list(PROBLEM_WEIGHT.keys())

    # https://bootstrap-vue.js.org/docs/components/table
    def row_variant(row):
        if row["grade"] is not None and row["grade"] >= row["mean"]:
            path.remove(row.name)
            return "success"
        return "danger"
    df["_rowVariant"] = df.apply(row_variant, axis=1)
    df = df.round(2)

    df.index.rename('Learning Object', inplace=True)
    df.rename(columns={'grade': 'Score', 'mean': 'Avg. Score'}, inplace=True)
    df = df.round(2)
    return JsonResponse({
        "table": df.reset_index().to_dict(orient='records'),
        "path": path
    }, safe=False)
