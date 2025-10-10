from django.contrib import admin
from .models import Classroom, Enrollment

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id','name','day_of_week','time_range')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id','student','classroom','joined_on')
    autocomplete_fields = ('student','classroom')
