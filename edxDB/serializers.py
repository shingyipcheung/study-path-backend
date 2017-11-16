from rest_framework import serializers
from edxDB.models import *
import json

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'lo_points_json']

    def to_representation(self, instance):
        points = instance.get_lo_points()
        los = [x.name for x in LearningObject.objects.all()]
        #print(Student.objects.first().get_lo_points())
        representation = {los[int(k) - 1]: v for k, v in points.items()}
        representation['student_id'] = instance.student_id

        return representation
