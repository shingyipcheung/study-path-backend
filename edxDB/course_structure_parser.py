import json
import re
import warnings


def truncate_by_special_char(key):
    # intput:
    # xxxx\xxxx\yyyy or xxxx@xxxx@yyyy
    # output:
    # yyyy
    # \W: special character
    # \W: special character
    return re.split("[\W]", key)[-1]


def chapter_tag(tagstr: str):
    return int(tagstr.split("-")[0])


class Node:
    def __init__(self, parent=None, key="", category="", meta=None, tag=""):
        self.parent = parent
        self.hash = key  # course item hash
        self.category = category
        self.meta = meta
        self.tag = tag  # the hierarchical ith child
        self.children = []

    def __repr__(self):
        return '<tree node representation>'

    def __str__(self, level=0):
        # ret = "\t" * level + repr(self.tag) + "\n"
        ret = "\t" * level + repr(self.display_name) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __hash__(self):
        return self.hash

    @property
    def display_name(self):
        if "display_name" in self.meta and self.meta["display_name"] != "":
            return self.meta["display_name"]
        return self.hash

    @property
    def chapter(self):
        curr = self.parent
        while curr is not None and curr.category != "chapter":
            curr = curr.parent
        if curr is not None:
            return curr.display_name
        return None

    def get_ancestor(self, category):
        curr = self.parent
        while curr is not None and curr.category != category:
            curr = curr.parent
        if curr is not None:
            return curr
        return None

    @property
    def chapter_tag(self):
        # re.search("(\d)+-.*", self.tag).group(1)
        return chapter_tag(self.tag)


class Tree:
    def __init__(self, node: Node):
        self.root = node

    def __str__(self):
        return self.root.__str__()

    @staticmethod
    def get_all_node_recursive(root, category, lst):
        if root.category == category:
            lst.append(root)
        for child in root.children:
            Tree.get_all_node_recursive(child, category, lst)
        return lst

    def get_all_node(self, category) -> list:
        return Tree.get_all_node_recursive(self.root, category, [])

    def hash_to_node(self, category) -> dict:
        nodes = self.get_all_node(category)
        return dict(zip([node.__hash__() for node in nodes], nodes))

    def hash_to_tag(self, category) -> dict:
        nodes = self.get_all_node(category)
        return dict(zip([node.__hash__() for node in nodes], [node.tag for node in nodes]))

    def hash_to_chapter_node(self, category) -> dict:
        nodes = self.get_all_node(category=category)
        # get the list of chapters w.r.t the video nodes
        belong_chapters = [node.chapter for node in nodes]
        keys = [node.__hash__() for node in nodes]
        return dict(zip(keys, belong_chapters))

    def problem_tag_to_weight(self) -> dict:
        problem_nodes = self.get_all_node("problem")
        # weight key check
        weight_exist = True
        problem_weight = {}
        for node in problem_nodes:
            if "weight" not in node.meta:
                problem_weight[node.tag] = None
                weight_exist = False
            else:
                problem_weight[node.tag] = node.meta["weight"]

        if weight_exist is False:
            warnings.warn("No weight index on course structure file. ALL weights are set to None")

        return problem_weight

    def problem_hash_to_graded_sequential(self) -> dict:
        problem_nodes = self.get_all_node("problem")
        graded_sequential = {}
        for node in problem_nodes:
            sequential_ancestor = node.get_ancestor("sequential")
            if sequential_ancestor is not None:
                if "graded" in sequential_ancestor.meta and sequential_ancestor.meta["graded"] is True:
                    if "weight" not in node.meta or "weight" in node.meta and node.meta["weight"] > 0:
                        graded_sequential[node.hash] = sequential_ancestor.meta["format"]
        return graded_sequential

    def chapter_tag_to_weight(self) -> dict:
        problem_tag_to_weight = self.problem_tag_to_weight()

        # chapter to sum weight
        chapter_to_sum_weight = {}
        for ptag, weight in problem_tag_to_weight.items():
            ctag = chapter_tag(ptag)
            if ctag in chapter_to_sum_weight:
                chapter_to_sum_weight[ctag] += problem_tag_to_weight[ptag]
            else:
                chapter_to_sum_weight[ctag] = problem_tag_to_weight[ptag]

        return chapter_to_sum_weight

    def sum_all_problem_weight(self) -> float:
        problem_tag_to_weight = self.problem_tag_to_weight()
        return sum(weight for weight in problem_tag_to_weight.values())


def recursive_parse(source_dict, key, parent=None, ith_child=0, preprocess_key=truncate_by_special_char):
    if key in source_dict:
        value = source_dict[key]

        if parent is None:
            tag = ''
        else:
            ith_str = str(ith_child).zfill(2)
            if parent.tag == '':
                tag = ith_str
            else:
                tag = '-'.join([parent.tag, ith_str])

        root = Node(parent=parent, key=preprocess_key(key),
                    category=value["category"], meta=value["metadata"], tag=tag)
        for i, child_key in enumerate(value["children"]):
            root.children.append(recursive_parse(source_dict, child_key, root, i))
        return root
    return None


def parse_course_structure(file):
    with open(file) as json_data:
        data = json.load(json_data)
        for key, value in data.items():
            if value["category"] == "course":
                root = recursive_parse(data, key)
                return Tree(root)
    return None


def main():
    tree = parse_course_structure('HKUSTx-COMP102x-2T2014-course_structure-prod-analytics.json')
    print(tree.root)
    # for n in tree.get_all_node("chapter"):
    #     print(n.display_name)
    # video_id_to_chapter = tree.hash_to_chapter_node("video")
    # problem_id_to_chapter = tree.hash_to_chapter_node("problem")
    # for k, v in problem_id_to_chapter.items():
    #     print(k, "->", v)


if __name__ == '__main__':
    main()
