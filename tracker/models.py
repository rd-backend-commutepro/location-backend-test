from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100, blank=True)
    device_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_id} ({self.name})'


class LocationLog(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(default=0.0)
    heading = models.FloatField(default=0.0)
    accuracy = models.FloatField(default=0.0)
    timestamp = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.device.device_id} @ {self.timestamp}'
