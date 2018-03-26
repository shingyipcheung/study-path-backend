from django.http import JsonResponse
import pandas as pd
import os
from .constants import PROBLEM_WEIGHT, VIDEO_DICT

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


def videos(request, concept):
    return JsonResponse(VIDEO_DICT[concept], safe=False)


def graph(request):
    df = read_df("risk_ratio.pkl")
    return JsonResponse(df.to_dict(orient='records'), safe=False)


def concepts(request):
    return JsonResponse(list(PROBLEM_WEIGHT.keys()), safe=False)


def means(request):
    df = read_df("concept_score_mean.pkl")
    return JsonResponse(df.round(2).to_dict(), safe=False)


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
    return JsonResponse(df.reset_index().to_dict(orient='records'), safe=False)


# https://gist.github.com/kachayev/5910538
def topological(graph):
    from collections import deque
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = 0
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == 0:
                raise ValueError("cycle")
            if sk == 1:
                continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = 1

    while enter:
        dfs(enter.pop())
    return list(order)


# BFS for Disconnected Graph
def BFS(graph):
    if len(graph) == 0:
        return []
    from collections import deque

    visited = set()
    result = list()

    for node in graph.keys():
        queue = deque()
        queue.append(node)
        if node not in visited:
            visited.add(node)
            while len(queue) != 0:
                v = queue.popleft()
                result.append(v)
                if v in graph:
                    for u in graph[v]:
                        if u not in visited:
                            visited.add(u)
                            queue.append(u)
    return result


def recommendation(request, student_id):
    df = read_df("student_concept_grade.pkl")
    student_id = int(student_id)
    student = df.loc[student_id]
    student = student.rename("grade")
    # ratio = read_df("risk_ratio.pkl")
    mean = read_df("concept_score_mean.pkl")
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
    # concept that below mean
    # below_mean = df[df["_rowVariant"] == "danger"].index.tolist()
    # edges that risk ratio > threshold
    # THRESHOLD = 2
    # ratio = read_df("risk_ratio.pkl")
    # critical_pair = ratio[ratio["value"] >= THRESHOLD]
    #
    # graph = {}
    #
    # def add_edge(row):
    #     if row["source"] not in below_mean:
    #         if row["target"] not in graph:
    #             graph[row["target"]] = []
    #     else:
    #         if row["source"] not in graph:
    #             graph[row["source"]] = []
    #         graph[row["source"]].append(row["target"])
    #
    # for concept in below_mean:
    #     pairs = critical_pair[critical_pair["target"] == concept]
    #     pairs.apply(add_edge, axis=1)

    # print(topological(graph))
    df.index.rename('Learning Object', inplace=True)
    df.rename(columns={'grade': 'Score', 'mean': 'Avg. Score'}, inplace=True)
    df = df.round(2)
    return JsonResponse({
        "table": df.reset_index().to_dict(orient='records'),
        "path": path
    }, safe=False)
