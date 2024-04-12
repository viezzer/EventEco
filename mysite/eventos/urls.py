from django.urls import path, include
from .views import EventEcoDetail, UpdateEventEcoDetail

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('<int:pk>/edit/', UpdateEventEcoDetail.as_view(), name="edit_eventeco"),
    path('<int:pk>/', EventEcoDetail.as_view(), name="eventeco_detail")
]