from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/attendance/', include('modules.attendance.urls')),
    path('', include('modules.lessons.urls')),  # simple root page
]
