from rest_framework import serializers
from .models import Device, LocationLog


class LocationUpdateSerializer(serializers.Serializer):
    """Accepts incoming location payload from Flutter app."""
    device_id = serializers.CharField(max_length=100)
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    speed = serializers.FloatField(default=0.0)
    heading = serializers.FloatField(default=0.0)
    accuracy = serializers.FloatField(default=0.0)
    timestamp = serializers.DateTimeField()


class LocationLogSerializer(serializers.ModelSerializer):
    """For reading logs back out."""
    device_id = serializers.CharField(source='device.device_id')

    class Meta:
        model = LocationLog
        fields = [
            'device_id', 'latitude', 'longitude',
            'speed', 'heading', 'accuracy',
            'timestamp', 'received_at'
        ]
