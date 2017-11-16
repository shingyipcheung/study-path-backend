from django.db import models
import json

# Create your models here.

# models of Students
class Student(models.Model):
    student_id = models.IntegerField()
    enroll_time = models.DateTimeField(null = True)
    # store the result of get_all_learning_object_points() in this field to speed up queries
    lo_points_json = models.CharField(max_length = 100)

    # https://stackoverflow.com/questions/22340258/django-list-field-in-model
    def get_lo_points(self):
        return json.loads(self.lo_points_json)

    def set_lo_points(self, d):
        self.lo_points_json = json.dumps(d)

    # get the point earned on this learning object by this student
    def get_learning_object_points(self, lo):
        # lo should be LearningObject class and in the database
        # -1 means student haven't touched this learning object
        points = -1
        # each contribution means a question
        for c in lo.contribution_set.all():
            records = Record.objects.filter(student=self, question=c.question)
            # if the student hasn't answered this question
            if records.count() <= 0:
                continue
            # the max score this student has got on this question
            max_score = records.aggregate(score = models.Max('score'))['score']
            # student has touched this learning object
            if points < 0:
                points = 0
            points += max_score * c.ratio
        return points

    # get all learning objects points and return as a dictionary
    def get_all_learning_object_points(self):
        los = LearningObject.objects.all()
        points_dict = {}
        for lo in los:
            points_dict[lo.id] = self.get_learning_object_points(lo)
        return points_dict

# The learning objects of the courses.
class LearningObject(models.Model):
    name = models.CharField(max_length = 100)
    children = models.ManyToManyField("LearningObject", through = "Dependency", through_fields = ("parent_lo", "child_lo"))
    questions = models.ManyToManyField("Question", through = "Contribution", through_fields = ("learning_object", "question"))
    # total points for this learning object, calcilated from the related Contribution
    total_points = models.FloatField(null=True)
    # average points students get for this learning object
    average_points = models.FloatField(null=True)

    # These two functions are to update the 2 attributes above. only for update.
    def get_total_points(self):
        total_points = 0
        contributions = self.contribution_set.all()
        for c in contributions:
            total_points += c.ratio * c.question.max_score
        return total_points

    def get_average_points(self):
        average_points = 0
        contributions = self.contribution_set.all()
        for c in contributions:
            average_points += c.ratio * c.question.average_score
        return average_points

# only care about the graded problem within the semester
# (exclude the final questions and course reviews)
class Question(models.Model):
    file_name = models.CharField(max_length = 40)
    name = models.CharField(max_length = 100)
    max_score = models.FloatField()
    average_score = models.FloatField(null = True)

    def __str__(self):
        return self.name

    # For update the average_score above
    def get_average_score(self):
        records = self.record_set.all()
        total = 0.0
        count = 0.0
        for r in records:
            total += r.score
            count += 1.0
        if count == 0:
            return 0
        return total / count

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
