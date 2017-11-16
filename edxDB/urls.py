from django.conf.urls import url
from edxDB import views

urlpatterns = [
    url(r'^students/$', views.student_lo),
]
