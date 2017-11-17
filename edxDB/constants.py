# CONSTANT file

# problem to concept mapping
# many-to-many mapping
# you can use either one problem map to multiple concepts or
# one concept map to multiple problems
# however, the latter one is more appropriate for course designer
PROBLEM_WEIGHT = {
    "primitive_type": {
        '27a9876d7b714ae2b190e085857f4663': 1,
        'd5146af552274e4fb0527e97365b970c': 1,
        'cb4951aacaf648af88111b92d51440a4': 1,
        'd8600cf2a37a4f72a0aa4f254ee48455': 1
    },
    "variable": {
        'd3c1c1156dca420789b8bc0c833bf34a': 1
    },
    "operator": {
        '821bc15e0bed4e179ddc1c802b313eec': 1,
        'd1dfc14002cc41aab7a6cb31c3b6aa18': 1
    },
    "array": {
        'b45eb7410f12464ca3ba317d3fe46090': 1,
        '662484c514da42fea6a0a3780cec52f8': 1,
        'c1843fce4a3d42bab62f4a3c73ac6578': 1
    },
    "nd_array": {
        '17333909316240a0b59c679ab6c7ede1': 1,
        '8a899a153c85442793502aacb6d8aaac': 1
    },
    "string": {
        '0eccc6a390844ac9b8d5a92eef410848': 1,
        '265841130b8040bda63f205373944857': 1,
        '050ab84aae0840c8863053c6bd287f94': 0.5,
        '7d10011449bf4ce7b07df4fbe8422472': 0.8
    },
    "branch": {
        '180f93865c8b40d6a06f6dca6d2bf741': 1,
        '2879f5a8c65745bc8e945bb9ee7e798a': 1
    },
    "loop": {
        '0792a1e4ce5c428eafbb9467566c7a1c': 0.5,
        'b80ac7b29ad74e71bc334c2b3a072315': 1,
        '29ad9230a63f45eea3f5a325b33d2393': 1,
        '050ab84aae0840c8863053c6bd287f94': 0.2
    },
    "object_class": {
        '5e4d503eb8084cca9f8ebf5397921420': 0.4,
        'c9fec2c277df4bb89862b4f5f913b910': 0.5
    },
    "instance_variable": {
        '5e4d503eb8084cca9f8ebf5397921420': 0.3
    },
    "method": {
        '5e4d503eb8084cca9f8ebf5397921420': 0.3,
        '0792a1e4ce5c428eafbb9467566c7a1c': 0.5,
        '050ab84aae0840c8863053c6bd287f94': 0.3,
        '7d10011449bf4ce7b07df4fbe8422472': 0.2,
        'c9fec2c277df4bb89862b4f5f913b910': 0.5,
        '7f03405fb68145bf9ca94c2f6a2b250b': 1,
        'f317883654264eb2ba5485e991bdeac3': 1
    },
    "recursion": {
        'a7b066155ce5435984635e11f8a666f3': 1,
        'f819e50f696a48678cad2fadd4b5f485': 1,
        '6031b3c8f6cd4cf1a04d009273e298db': 1,
        '6d6a425cf0da4a268f637fb33572d1a3': 1
    }
}

# sparse graph using adjacency list
CONCEPT_EDGES = {
    "primitive_type": ["operator", "array", "variable"],
    "operator": ["branch"],
    "branch": ["loop"],
    "array": ["nd_array", "string"],
    "variable": ["array", "instance_variable"],
    "object_class": ["instance_variable", "method"],
    "instance_variable": ["method"],
    "method": ["recursion"]
}

# preprocess grade file
GRADE_FILE = "data/HKUSTx-COMP102x-2T2014-courseware_studentmodule-prod-analytics.sql"
