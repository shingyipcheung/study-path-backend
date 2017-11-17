from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^graph/$', views.index, name='index'),
    url(r'^problem/(?P<problem_id>\w+)/$', views.problem, name='problem')
]