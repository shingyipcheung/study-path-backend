from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^concepts/$', views.concepts, name='concepts'),
    url(r'^means/$', views.means, name='means'),
    url(r'^graph/$', views.graph, name='graph'),
    url(r'^problem/(?P<problem_id>\w+)/$', views.problem, name='problem'),
    url(r'^concept_score/(?P<student_id>\d+)/$', views.concept_score, name='concept_score'),
    url(r'^concept_score/all/$', views.concept_score_all, name='concept_score_all'),
    url(r'^recommendation/(?P<student_id>\d+)/$', views.recommendation, name='recommendation'),
]
