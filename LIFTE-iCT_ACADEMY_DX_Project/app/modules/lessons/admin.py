from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id','classroom','held_on','topic')
    list_filter = ('classroom','held_on')
