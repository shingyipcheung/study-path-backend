import pandas as pd
import json
from pprint import pprint
import numpy as np

df = pd.read_csv("./data/actions.sql", sep="\t")

with open("./data/course_structure.json", "r") as f:
    idx_info = json.load(f)

df["module_id"] = df["module_id"].map(lambda x: idx_info.get(x, x))


pprint(df[df['module_type'] == "course"].sort_values('created').head(100))
'''
# analysis for module type and state
for i in range(1, 1000):
    row = df.values[i]
    print(row[1])
    print()
    try:
        pprint(json.loads(row[4]))
    except:
        print("fail to decode one row")
    print("##################################")
'''
'''
# analysis for distinct values
unique_values = df.course_id.unique()
print(np.sort(unique_values))
try:
    print(unique_values.shape)
except:
    print("### it's a list ###")
    print(len(unique_values))
'''
'''
# student analysis
# print(df.groupby("student_id").count().sort_values("id"))
student_act = df[df['student_id']==4369464].sort_values("modified")
student_act_values = student_act.values
for row in student_act_values:
    print(row[7])
    print()
    print(row[2])
    print()
    print(row[1])
    print()
    try:
        pprint(json.loads(row[4]))
    except:
        print("fail to decode one row")
    print("##################################")
'''
# grade analysis
'''
student_act = df[(df['student_id']==4369464) & (df['module_type']=='problem')].sort_values("modified")
student_act_values = student_act.values
for row in student_act_values:
    if (np.isnan(row[5])) and (np.isnan(row[8])):
        pass
    else:
        print(row[7])
        print()
        pprint(row[2])
        print()
        #print(row[1])
        #print()
        print("grade: " + str(row[5]) + "/" + str(row[8]))
        print("###########")
'''











pass
