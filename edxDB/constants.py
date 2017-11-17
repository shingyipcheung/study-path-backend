objects_mapping = {
    "primitive_type": 1,
    "variable": 2,
    "operator": 3,
    "array": 4,
    "nd_array": 5,
    "string": 6,
    "branch": 7,
    "loop": 8,
    "object_class": 9,
    "instance_variable": 10,
    "method": 11,
    "recursion": 12}

week_mapping = {
    1: [2014, 6, 26],
    2: [2014, 7, 3],
    3: [2014, 7, 10],
    4: [2014, 7, 17],
    5: [2014, 7, 24],
    6: [2014, 7, 31],
    7: [2014, 8, 7],
    8: [2014, 8, 14],
    9: [2014, 8, 21],
    10: [2014, 8, 28]
}

# the corresponding learning objects are defined above
lo_dependency_pairs = [
    "1 3",
    "1 4",
    "1 2",
    "3 7",
    "7 8",
    "4 5",
    "4 6",
    "2 4",
    "2 10",
    "10 11",
    "9 10",
    "9 11",
    "11 12"
]
