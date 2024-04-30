from django.urls import path, include
from .views import EventEcoDetail, UpdateEventEcoDetail, enviar_email_evento

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("email/", enviar_email_evento, name="email"),
    path('<int:pk>/edit/', UpdateEventEcoDetail.as_view(), name="edit_eventeco"),
    path('<int:pk>/', EventEcoDetail.as_view(), name="eventeco_detail")
]