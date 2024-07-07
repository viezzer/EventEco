from django.urls import path
from .views import EventEcoDetail, enviar_email_evento, search_event

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("email/", enviar_email_evento, name="email"),
    path("search/", search_event, name="search"),
    path('<int:pk>/', EventEcoDetail.as_view(), name="eventeco_detail")
]