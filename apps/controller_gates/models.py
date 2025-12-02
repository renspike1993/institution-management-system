from django.db import models


class TurnstileAttendanceLog(models.Model):
    DIRECTION_CHOICES = [
        ('IN', 'Entry'),
        ('OUT', 'Exit'),
    ]

    STATUS_CHOICES = [
        ('AUTHORIZED', 'Authorized'),
        ('UNAUTHORIZED', 'Unauthorized'),
    ]

    # Basic identity info (from RFID / Face / ID)
    person_id = models.CharField(max_length=50)   # RFID, Student No, Employee ID
    full_name = models.CharField(max_length=150)

    # Turnstile info
    gate_name = models.CharField(max_length=100)  # e.g. Gate 1, Main Entrance
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES)

    # Access result
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional extra info
    remarks = models.TextField(blank=True, null=True)
    snapshot = models.ImageField(upload_to="turnstile_snapshots/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Turnstile Attendance Log"
        verbose_name_plural = "Turnstile Attendance Logs"

    def __str__(self):
        return f"{self.full_name} - {self.gate_name} - {self.timestamp}"
