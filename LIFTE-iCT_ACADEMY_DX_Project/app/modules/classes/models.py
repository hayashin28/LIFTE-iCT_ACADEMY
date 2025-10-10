from django.db import models
from modules.students.models import Student

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=16, blank=True)  # e.g., Mon
    time_range = models.CharField(max_length=32, blank=True)   # e.g., 17:00-18:00
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    joined_on = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('student','classroom')
