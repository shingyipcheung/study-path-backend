from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os
from wsgiref.util import FileWrapper
from django.views.decorators.csrf import csrf_exempt

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


def index(request):
    df = read_df("risk_ratio.pkl")
    return JsonResponse(df.to_dict('records'), safe=False)
    # filename = settings.MEDIA_ROOT + '/' + 'output1.csv'
    # filename = "C:/Users/Wind/PycharmProjects/elearning-project/mysite/study_plan/force.csv"
    # wrapper = FileWrapper(open(filename))
    # response = HttpResponse(wrapper, content_type='text/csv')
    # response['Content-Disposition'] = "attachment; filename=%s" % filename
    # return response


def problem(request, problem_id):
    df = read_df("problem_records.pkl")
    problem_df = df[df["problem_id"] == problem_id]
    sorted_grade = problem_df[["student_id", "grade"]].sort_values(by=["grade"])
    return JsonResponse(sorted_grade.to_dict(orient="list"), safe=False)

    # df = pd.read_pickle("problem_records.pkl")
    # max_grade = df.groupby("problem_id").agg({"max_grade": "max"})
    # df['max_grade'] = df['problem_id'].map(lambda id: max_grade.loc[id, 'max_grade'])
    # # drop max_grade if max_grade still be nan
    # df.dropna(subset=["max_grade"], inplace=True)
    # # fill grade with value 0
    # df.fillna(value=0, inplace=True)
