from .possible_path_generator import *
from .diversifier import *
import pickle

class DiversifiedResultsLoader:
    PRECOMPUTED_PATH = {  "answer1": {'primitive_type'},
                          "answer2": {'object_class'},
                          "answer3": {},
                          "answer4": {'primitive_type', 'operator'},
                          "answer5": {'primitive_type', 'variable'},
                          "answer6": {'primitive_type', 'object_class'},
                          "answer7": {'primitive_type', 'operator', 'object_class'},
                          "answer8": {'primitive_type', 'operator', 'branch'},
                          "answer9": {'primitive_type', 'operator', 'variable'},
                          "answer10": {'primitive_type', 'variable', 'object_class'},
                          "answer11": {'primitive_type', 'variable', 'array'},
                          "answer12": {'primitive_type', 'variable', 'object_class', 'operator'},
                          "answer13": {'primitive_type', 'variable', 'array', 'object_class'},
                          "answer14": {'primitive_type', 'variable', 'array', 'operator'},
                          "answer15": {'primitive_type', 'variable', 'object_class', 'instance_variable'}
                       }
    CONCEPT_EDGES = {
        "primitive_type": ["operator", "array", "variable"],
        "operator": ["branch"],
        "branch": ["loop"],
        "array": ["nd_array", "string"],
        "variable": ["array", "instance_variable"],
        "object_class": ["instance_variable", "method"],
        "instance_variable": ["method"],
        "method": ["recursion"],
        "loop": [],
        "nd_array": [],
        "string": [],
        "recursion": []    
    }
    PPG = PossiblePathGenerator()
    diversifier = Diviersifier()
    def load(self, learned_object):
        if len(learned_object) == 0:
            file_name = './edxDB/diversified/answer/answer3.pkl'
            with open(file_name, 'rb') as f:
                node_name_map, res = pickle.load(f)
            L = []
            for seq in res:
                l = []
                for idx in seq:
                    l.append(node_name_map[idx])
                L.append(l)
            return L
        else:
            file_name = ''
            for key, value in self.PRECOMPUTED_PATH.items():
                if(learned_object.issubset(value)):
                    file_name = './edxDB/diversified/answer/' + key + '.pkl'
                    break
            if(file_name != ''):
                with open(file_name, 'rb') as f:
                    node_name_map, res = pickle.load(f)

                L = []
                for seq in res:
                    l = []
                    for idx in seq:
                        l.append(node_name_map[idx])
                    L.append(l)
                return L
            else:
                unlearn_concepts = self.CONCEPT_EDGES.copy()
                for concept in learned_object:
                    unlearn_concepts.pop(concept, None)
                all_nodes, _, _ = self.PPG.find_node_set(unlearn_concepts)
                node2ind, indmap = self.PPG.create_dependency_map_with_index(unlearn_concepts, all_nodes)
                ret = self.PPG.permutation(all_nodes, node2ind, indmap)
                possible_sequences = [list(elem) for elem in ret]
                if len(possible_sequences) > 200:
                    _, Q = self.diversifier.diversify(possible_sequences, r=len(learned_object))
                else:
                    Q = possible_sequences
                L = []
                node_name_map = list(all_nodes)
                for seq in Q:
                    l = []
                    for idx in reversed(seq):
                        l.append(node_name_map[idx])
                    L.append(l)
                return L

