from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
