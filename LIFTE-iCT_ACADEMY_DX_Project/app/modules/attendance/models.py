from django.db import models
from django.utils import timezone
from uuid import uuid4
from modules.lessons.models import Lesson
from modules.students.models import Student

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present','present'),
        ('late','late'),
        ('absent','absent'),
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_at = models.DateTimeField(auto_now_add=True)
    qr_log = models.TextField(blank=True)

    class Meta:
        unique_together = ('lesson','student')

class QrTicket(models.Model):
    token = models.UUIDField(default=uuid4, unique=True, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        now = timezone.now()
        return (self.used_at is None) and (self.expires_at > now)
