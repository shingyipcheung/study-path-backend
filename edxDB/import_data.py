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
import numpy as np
import datetime
# handle the problems about the time zone
from django.utils import timezone
import pytz
# for formatted output
from pprint import pprint


from edxDB.models import *
from edxDB.constants import *
from edxDB.helpers import *

################################################################
# This variable should store the location of all the json file.#
# Please change it accordingly.                                #
################################################################
data_dir = r"./data"

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
            print(name)
            if q == None:
                # create Question
                q = Question(name = name, file_name = file_name, max_score = max_score)
                q.save()
                create_counter += 1
            else:
                # update Question
                q.name = name
                q.max_score = max_score
                update_counter += 1
            # update the contributions
            for lo_name, ratio in contribution_dict.items():
                # LearningObject should exist
                # normal get() will raise exception if record does not exist.
                print(lo_name, ratio)
                lo = LearningObject.objects.get(name = lo_name)
                c = get_or_none(Contribution, question = q, learning_object = lo)
                if c == None:
                    # create Contribution
                    c = Contribution(question = q, learning_object = lo, ratio = ratio)
                    c.save()
                else:
                    # for future udpate
                    pass

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
            # for future udpate
            update_counter += 1
    print("Total %d Dependency created." % create_counter)
    print("Total %d Dependency updated." % update_counter)

# import records of the students doing questions
# There is a PDF file describe the structure of the actions.sql
def import_records(file_name = "actions.sql"):
    os.chdir(data_dir)
    actions = pd.read_csv(file_name, sep = "\t")
    problem_records = actions[actions['module_type'] == "problem"]
    problem_records = problem_records[problem_records['grade'].notnull()]
    print(problem_records['id'].count()) # 623909 records, need to filter more
    # df[df.apply(lambda x: x['b'] > x['c'], axis=1)] # try this function next
    counter = 0
    create_counter = 0
    # For bulk create in django
    create_list = []
    for i, problem_r in problem_records.iterrows():
        problem_file_name = problem_r['module_id'].split('/')[-1]
        score = problem_r['grade']
        created = datetime.datetime.strptime(problem_r['created'], "%Y-%m-%d %H:%M:%S")
        # https://stackoverflow.com/questions/34817109/python-string-to-django-timezone-aware-datetime
        created = pytz.utc.localize(created)
        # find the related objects
        question = get_or_none(Question, file_name = problem_file_name)
        student = get_or_none(Student, student_id = problem_r['student_id'])
        if question == None or student == None:
            if question == None:
                continue
                #print("question %s not found" % (problem_file_name))
            if student == None:
                continue
                #print("student %s not found" % (problem_r['student_id']))
        elif score != None: # if the score is null, ignore it
            #print(score, type(score))
            new_record = get_or_none(Record, question = question, student = student, time = created)
            # create
            if new_record == None:
                new_record = Record(question = question, student = student, score = score, time = created)
                create_list.append(new_record)
                create_counter += 1
                #print("Found question: %s" % (problem_file_name))
            else:
                pass
        counter += 1
        #print(create_counter)
        if counter % 1000 == 0:
            print("traversed %d records." % counter)
        # save once for every 1000 records
        if create_counter % 1000 == 0 and create_counter != 0:
            print("saving the first %d records. " % create_counter)
            Record.objects.bulk_create(create_list)
            create_list = []

#####################################################
# The main entry to import the data to the database #
#####################################################
def import_all_data():
    # if create the database from empty, do the following sequentially after migrations
    #import_learning_objects()
    #import_student()
    #import_questions()
    #import_dependency()
    #import_records()
    print("import done")

# Set average score for each question to speed up queries
def set_question_average_score():
    questions = Question.objects.all()
    for q in questions:
        average_score = q.get_average_score()
        q.average_score = average_score
        print("%0.2f / %0.2f" % (average_score, q.max_score))
        q.save()

# set total points and average points for each learning object from its related questions
def set_learning_objects_total_and_average():
    los = LearningObject.objects.all()
    for lo in los:
        total_points = lo.get_total_points()
        average_points = lo.get_average_points()
        print(lo.name, average_points, total_points)
        lo.total_points = total_points
        lo.average_points = average_points
        lo.save()

# delete the students who haven't answered any questions
def delete_inactive_students():
    count = 0
    for s in Student.objects.all():
        if s.record_set.count() <= 0:
            count += 1
            #print(s.student_id)
            s.delete()
            if count % 100 == 0:
                print("deleting %d students" % count)
    print("delete total %d inactive students" % count)

# calculate all students earnings on the learning objects and set the result to the related attributes
def set_student_points_on_learning_objects():
    students = Student.objects.all()
    count = 0
    for s in students:
        s.set_lo_points( s.get_all_learning_object_points() )
        count += 1
        s.save()
        if count % 100 == 0:
            print(count)

def main_entry():
    set_student_points_on_learning_objects()
    return
