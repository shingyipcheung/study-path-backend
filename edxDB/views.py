from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from edxDB.models import *
from edxDB.serializers import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def student_lo(request):
    print(request.method)
    if request.method == "OPTIONS":
        return HttpResponse(status = 200)
    if request.method == 'GET':
        students = Student.objects.all()[0:500]
        serializer = StudentSerializer(students, many=True)
        total_points = [x.total_points for x in LearningObject.objects.all()]
        learning_objects = [x.name  for x in LearningObject.objects.all()]
        return JSONResponse({
            "students":serializer.data,
            "total_points": total_points,
            "learning_objects": learning_objects
            })
    else:
        return HttpResponse(status = 404)

# Create your views here.
