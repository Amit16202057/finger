# fingerprint_attendance/models.py

from django.db import models

class Attendance(models.Model):
    name = models.CharField(max_length=255)
    fingerprint_template = models.BinaryField()

    class Meta:
        app_label = 'fingerprint_attendance'
