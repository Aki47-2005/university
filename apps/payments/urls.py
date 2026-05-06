from django.urls import path

from . import views

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path("new/", views.payment_create, name="payment_create"),
    path("<int:pk>/edit/", views.payment_update, name="payment_update"),
    path("clearance/", views.clearance_list, name="clearance_list"),
    path("clearance/<int:pk>/edit/", views.clearance_update, name="clearance_update"),
]
