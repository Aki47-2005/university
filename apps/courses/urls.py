from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("new/", views.course_create, name="course_create"),
    path("<int:pk>/edit/", views.course_update, name="course_update"),
    path("<int:pk>/delete/", views.course_delete, name="course_delete"),
    path("register/", login_required(views.register_course), name="register_course"),
    path("slip/", login_required(views.registration_slip), name="registration_slip"),
]
