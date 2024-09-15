from django.db import models

class PerformanceMarketingGroupMessaages(models.Model):
    message = models.CharField(max_length=1000)
    timestamp = models.CharField(max_length=100)  # You can adjust max_length based on the timestamp format

    def __str__(self):
        return f"Message: {self.message} at {self.timestamp}"