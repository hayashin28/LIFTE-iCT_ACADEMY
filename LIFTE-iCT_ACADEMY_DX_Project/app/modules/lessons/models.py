from django.db import models
from modules.classes.models import Classroom

class Lesson(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    held_on = models.DateField()
    topic = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.classroom.name} #{self.id} ({self.held_on})"
