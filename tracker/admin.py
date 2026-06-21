from django.contrib import admin
from .models import Device, LocationLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'created_at', 'location_count']
    search_fields = ['device_id', 'name']
    ordering = ['-created_at']

    def location_count(self, obj):
        return obj.logs.count()
    location_count.short_description = 'Total Logs'


@admin.register(LocationLog)
class LocationLogAdmin(admin.ModelAdmin):
    list_display = ['device', 'latitude', 'longitude',
                    'speed', 'accuracy', 'timestamp', 'received_at']
    list_filter = ['device']
    search_fields = ['device__device_id', 'device__name']
    ordering = ['-timestamp']
    readonly_fields = ['received_at']
