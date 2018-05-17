from functools import lru_cache
import pickle
from .diversifier import Diversifier
from .topological_all import Graph
from edxDB.constants import CONCEPT_EDGES, CONCEPTS


@lru_cache()
def index_of(concept):
    return CONCEPTS.index(concept)


def index(i):
    return CONCEPTS[i]


# convert [concept1, ...] to [concept1_index, ...]
def str2index(path):
    return [index_of(concept) for concept in path]


# convert [concept1_index, ...] to [concept1, ...]
def index2str(path):
    return [index(i) for i in path]


class PathsLoader:
    def __init__(self):
        self.diversified_paths = None
        self.load_pickle()

    def load_pickle(self):
        try:
            with open("diversified_path.pkl", "rb") as f:
                self.diversified_paths = pickle.load(f)
        except FileNotFoundError:
            self.preprocess()

    def load(self):
        # convert back to string paths
        return [index2str(path) for path in self.diversified_paths]

    def preprocess(self):
        print("preprocess diversified paths...")
        # all possible paths of topological sort
        paths = Graph(CONCEPT_EDGES).topological_all()
        # convert back to index paths
        paths = [str2index(path) for path in paths]
        diversifier = Diversifier()
        self.diversified_paths, _ = diversifier.diversify(paths)
        # serialize paths
        with open("diversified_path.pkl", 'wb') as f:
            pickle.dump(self.diversified_paths, f, pickle.HIGHEST_PROTOCOL)
