from django.urls import path
from django.http import HttpResponse

def index(request):
    return HttpResponse("LIFTE-iCT ACADEMY DX — MVP is running." )

urlpatterns = [
    path('', index),
]
