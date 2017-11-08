from django.db import models

# Create your models here.

# models of Students
class Student(models.Model):
    student_id = models.IntegerField()
    enroll_time = models.DateTimeField(null = True)

# The learning objects of the courses.
class LearningObject(models.Model):
    name = models.CharField(max_length = 100)
    children = models.ManyToManyField("LearningObject", through = "Dependency", through_fields = ("parent_lo", "child_lo"))

# only care about the graded problem within the semester
# (exclude the final questions and course reviews)
class Question(models.Model):
    file_name = models.CharField(max_length = 40)
    name = models.CharField(max_length = 100)
    max_score = models.FloatField()

# the records of student doing the problems
# class for many to many relationship between Student and Question
class Record(models.Model):
    student = models.ForeignKey(Student)
    question = models.ForeignKey(Question)
    # attributes
    score = models.FloatField()
    time = models.DateTimeField()

# Contribution of problems to learning objects
# class for many to many relationship between Problem and LearningObject
class Contribution(models.Model):
    question = models.ForeignKey(Question)
    learning_object = models.ForeignKey(LearningObject)
    # ratio of the contirbution of the problem to the learning object
    ratio = models.FloatField()

# Dependency graph within the learning objects
# store the risk ratio between the parent and child learning objects
class Dependency(models.Model):
    parent_lo = models.ForeignKey(LearningObject)
    child_lo = models.ForeignKey(LearningObject, related_name = "child_learning_object")
    risk_ratio = models.FloatField()


'''
# models about course structure
# structure: Course -> chapter -> sequential -> vertical -> problem html video
class Chapter(models.Model):
    # id is the full id including "i4x://HKUSTx/COMP102x/chapter"
    id = models.CharField(max_length = 100, primary_key = True)
    display_name = models.CharField(max_length = 60)
    start = models.DateTimeField()

class Sequential(models.Model):
    id = models.CharField(max_length = 100, primary_key = True)
    parent = models.ForeignKey(Chapter)

    display_name = models.CharField(max_length = 60)
    start = models.DateTimeField()
    due = models.DateTimeField()
    format = models.CharField(max_length = 60)
    graded = models.BooleanField()

class Vertical(models.Model):
    id = models.CharField(max_length = 100, primary_key = True)
    parent = models.ForeignKey(Sequential)

    display_name = models.CharField(max_length = 60)

class Problem(models.Model):
    id = models.CharField(max_length = 100, primary_key = True)
    parent = models.ForeignKey(Vertical)

    display_name = models.CharField(max_length = 60)
    markdown = models.CharField(max_length = 60)
    max_attempts = models.IntegerField()
    showanswer = models.CharField(max_length = 30)
    weight = models.FloatField()
    submission_wait_seconds = models.IntegerField()

class Html(models.Model):
    pass

class Video(models.Model):
    pass
'''
