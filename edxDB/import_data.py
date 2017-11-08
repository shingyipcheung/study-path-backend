'''
Author: GU Qiao
Use this file in Django shell
python3 .\manage.py shell
> from edxDB.import_data import *
> main_entry()
'''

import os
import json
import pandas as pd
import datetime
# handle the problems about the time zone
from django.utils import timezone
import pytz

try:
    from models import *
    from constants import *
    from helpers import *
except:
    from .models import *
    from .constants import *
    from .helpers import *

# This variable should store the location of all the json file.
# Please change it accordingly.
data_dir = r"C:\code\uropedx\edxback\edxDB\data"

# import learning objects defined in the constants.py
def import_learning_objects():
    for k, v in objects_mapping.items():
        # avoid repeated insertion
        lo = get_or_none(LearningObject, name = k)
        if lo == None:
            print("Creating learning obejct: %s" % (k))
            lo = LearningObject()
            lo.name = k
            lo.id = v
            lo.save()
        else:
            print("Learning Object %s exists" % (k))

# import student from student_enrollment.sql
def import_student(file_name = "student_enrollment.sql"):
    os.chdir(data_dir)
    students_df = pd.read_csv(file_name, sep='\t')
    # hold 2 counters for the traversal
    create_counter = 0
    update_counter = 0
    for i, stu_record in students_df.iterrows():
        # The attributes to be created or updated
        # format the datetime from string
        created = datetime.datetime.strptime(stu_record['created'], "%Y-%m-%d %H:%M:%S")
        # https://stackoverflow.com/questions/34817109/python-string-to-django-timezone-aware-datetime
        created = pytz.utc.localize(created)

        # avoid repeat
        stu = get_or_none(Student, student_id = stu_record['user_id'])
        if stu == None:
            #print("Creating Student: %s" % (stu_record['user_id']))
            stu = Student()
            stu.student_id = stu_record['user_id']
            stu.enroll_time = created
            create_counter += 1
        else:
            stu.enroll_time = created
            update_counter += 1
            #print("Student %s exists." % (stu_record['user_id']))
        stu.save()
        print("Total %d Students created." % create_counter)
        print("Total %d Students updated." % update_counter)

# import questions. Create or update the Question and add the contribution to the LearningObject
# sample:
# [0]name:"Week 01 Graded Problem Task 2",
# [1]file_name:"46e45e1fc5e24dd2b9e8a93382e97f5b",
# [2]max_score:1,
# [3]contribution dict:{}
def import_questions(file_name = "questions.json"):
    os.chdir(data_dir)
    with open(file_name) as data_file:
        data = json.load(data_file)
        create_counter = 0
        update_counter = 0

        for i, q_record in enumerate(data):
            name = q_record[0]
            file_name = q_record[1]
            max_score = q_record[2]
            contribution_dict = q_record[3]
            # file_name should be unique
            q = get_or_none(Question, file_name = file_name)
            if q == None:
                # create Question
                q = Question(name = name, file_name = file_name, max_score = max_score)
                q.save()
                create_counter += 1
                for lo_name, ratio in contribution_dict.items():
                    # LearningObject should exist
                    # normal get() will raise exception if record does not exist.
                    lo = LearningObject.objects.get(name = lo_name)
                    c = get_or_none(Contribution, question = q, learning_object = lo)
                    if c == None:
                        # create Contribution
                        c = Contribution(question = q, learning_object = lo, ratio = ratio)
                        c.save()
                    else:
                        # don't handle
                        pass
            else:
                # update Question
                q.name = name
                q.max_score = max_score
                update_counter += 1

        print("Total %d Questions created." % create_counter)
        print("Total %d Questions updated." % update_counter)

# Create Dependency models
# related data are defined in constants
def import_dependency():
    create_counter = 0
    update_counter = 0
    for lo_pair in lo_dependency_pairs:
        parent_lo_id, child_lo_id = lo_pair.split(" ")
        print(parent_lo_id, child_lo_id)
        # LearningObject should exist, ore Exception
        parent_lo = LearningObject.objects.get(id = parent_lo_id)
        child_lo = LearningObject.objects.get(id = child_lo_id)
        d = get_or_none(Dependency, parent_lo = parent_lo, child_lo = child_lo)
        if d == None:
            d = Dependency(parent_lo = parent_lo, child_lo = child_lo, risk_ratio = 0)
            d.save()
            create_counter += 1
        else:
            # don't handle
            update_counter += 1
    print("Total %d Dependency created." % create_counter)
    print("Total %d Dependency updated." % update_counter)

def main_entry():
    #import_learning_objects()
    #import_student()
    #import_questions()
    import_dependency()
    print("import done")
