from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", login_required(views.result_list), name="result_list"),
    path("new/", views.result_create, name="result_create"),
    path("<int:pk>/edit/", views.result_update, name="result_update"),
    path("<int:pk>/delete/", views.result_delete, name="result_delete"),
]
