from django.urls import path
from .views import mark_attendance

urlpatterns = [
    path('mark/<uuid:token>/', mark_attendance),
]
