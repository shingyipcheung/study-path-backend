from edxDB.df_loader import load_df
from heapq import nlargest
from functools import lru_cache
from edxDB.constants import CONCEPT_EDGES
from typing import List

from edxDB.diversified.diversified_paths_loader import PathsLoader


def generate_ratio_dict():
    risk_ratio = load_df("risk_ratio.pkl")
    ratio_dict = {}
    for index, row in risk_ratio.iterrows():
        v, u, w = row["source"], row["target"], row["value"]
        if v in ratio_dict:
            ratio_dict[v][u] = w
        else:
            ratio_dict[v] = {u: w}
    return ratio_dict


def paths_selection(fitness_func, paths: list, top_k=10) -> list():
    if len(paths) < top_k:
        top_k = len(paths)
    fitness = fitness_func(paths)
    # sort from high to low
    nlargest_indexes = nlargest(top_k, range(len(paths)), key=lambda i: fitness[i])
    # select top k paths
    # for i in nlargest_indexes:
    #     print(fitness[i])
    return [paths[i] for i in nlargest_indexes]


class PathEvaluator:
    # static variable for calculation
    risk_ratio = generate_ratio_dict()
    mean = load_df("concept_score_mean.pkl")
    student_grade = load_df("student_concept_grade.pkl")

    def __init__(self, student_id):
        self.student_id = student_id
        mean = PathEvaluator.mean
        # diff between student score and mean
        self.relative_score = (mean - self.__score().fillna(0)) / mean

    # === sample of calculate the score of some path ===
    def __score(self):
        return PathEvaluator.student_grade.loc[self.student_id]

    # === Wenlong's job ===
    @staticmethod
    @lru_cache(maxsize=None)
    def __calc_A(path):
        n = len(path)
        score = 0.0
        num_of_failed_descendants = [0] * n
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                # if node j is child of node i
                if path[i] in CONCEPT_EDGES and path[j] in CONCEPT_EDGES[path[i]]:
                    # child += 1
                    num_of_failed_descendants[i] += 1
                    num_of_failed_descendants[i] += num_of_failed_descendants[j]

        for i in range(n):
            score += 1.0 / (i + 1) * num_of_failed_descendants[i]

        return score

    def __calc_B(self, path):
        sum_of_product = 0.0

        for i, node in enumerate(path, start=1):
            sum_of_product += 1.0 / i * self.relative_score.ix[node]
        return sum_of_product

    @staticmethod
    @lru_cache(maxsize=None)
    def __calc_C(path):
        n = len(path)
        sum_of_product = 0.0
        for i in range(0, n):
            for j in range(i + 1, n):
                if (path[i] in PathEvaluator.risk_ratio) and (path[j] in PathEvaluator.risk_ratio[path[i]]):
                    distance = j - i
                    sum_of_product += 1.0 / distance * PathEvaluator.risk_ratio[path[i]][path[j]]

        return sum_of_product

    def evaluate(self, paths: List[List]):
        scores_a = [self.__calc_A(tuple(path)) for path in paths]
        scores_b = [self.__calc_B(path) for path in paths]
        scores_c = [self.__calc_C(tuple(path)) for path in paths]
        min_a, max_a = min(scores_a), max(scores_a)
        min_b, max_b = min(scores_b), max(scores_b)
        min_c, max_c = min(scores_c), max(scores_c)
        # min-max normalization
        diff_a = max_a - min_a
        diff_b = max_b - min_b
        diff_c = max_c - min_c
        if diff_a == 0:
            diff_a = 1
        if diff_b == 0:
            diff_b = 1
        if diff_c == 0:
            diff_c = 1

        scores = [((a - min_a) / diff_a +
                   (b - min_b) / diff_b +
                   (c - min_c) / diff_c
                   ) for a, b, c in zip(scores_a, scores_b, scores_c)]

        return scores
    # === Wenlong's job ends ===


# https://stackoverflow.com/questions/279561
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


@static_vars(paths=PathsLoader().load())
def generate_paths(student_id, top_k=10):
    evaluator = PathEvaluator(student_id=student_id)
    return paths_selection(evaluator.evaluate, generate_paths.paths, top_k=top_k)


def main():
    # example
    # student_grade = load_df("student_concept_grade.pkl")
    # student_ids = student_grade.index.tolist()
    # top_k_paths = [generate_paths(student_id=_id) for _id in student_ids[:100]]
    top_k_paths = generate_paths(student_id=342)
    print(top_k_paths)


if __name__ == '__main__':
    main()
