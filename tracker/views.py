from django.db.models import Count, Max
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import Device, LocationLog
from .serializers import LocationUpdateSerializer, LocationLogSerializer


class LocationUpdateView(APIView):
    """
    POST /api/location/update/
    Receives location from Flutter, saves to DB.
    """

    def post(self, request):
        serializer = LocationUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        # Get or create device (auto-registers new phones)
        device, created = Device.objects.get_or_create(
            device_id=data['device_id']
        )

        # Save location log
        LocationLog.objects.create(
            device=device,
            latitude=data['lat'],
            longitude=data['lng'],
            speed=data['speed'],
            heading=data['heading'],
            accuracy=data['accuracy'],
            timestamp=data['timestamp'],
        )

        return Response(
            {
                'status': 'ok',
                'device_id': device.device_id,
                'saved': True,
            },
            status=status.HTTP_201_CREATED
        )


class LocationHistoryView(APIView):
    """
    GET /api/location/history/?device_id=123&limit=50
    Returns last N locations for a device.
    """

    def get(self, request):
        device_id = request.query_params.get('device_id')
        limit = int(request.query_params.get('limit', 50))

        if not device_id:
            return Response(
                {'error': 'device_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            return Response(
                {'error': 'Device not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        logs = device.logs.all()[:limit]
        serializer = LocationLogSerializer(logs, many=True)
        return Response(serializer.data)


class HealthCheckView(APIView):
    """GET /api/health/ — Render uses this to check if server is alive."""

    def get(self, request):
        return Response({'status': 'ok'})


class CreateSuperUserView(APIView):
    """
    POST /api/create-superuser/
    ONE TIME USE — delete this endpoint after creating your admin.
    """

    def post(self, request):
        secret = request.data.get('secret')

        # Simple secret key check so random people can't hit this
        if secret != 'setup-2026-secret':
            return Response(
                {'error': 'Invalid secret'},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get('username', 'admin')
        email = request.data.get('email', '')
        password = request.data.get('password')

        if not password:
            return Response(
                {'error': 'password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': f'User "{username}" already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        return Response(
            {'status': 'ok', 'message': f'Superuser "{username}" created'},
            status=status.HTTP_201_CREATED
        )


class DeviceListView(APIView):
    """
    GET /api/devices/
    Returns all devices with their log count, for the dashboard sidebar.
    """

    def get(self, request):
        devices = Device.objects.annotate(
            log_count=Count('logs'),
            last_seen=Max('logs__timestamp'),
        ).order_by('-last_seen')

        data = [
            {
                'device_id': d.device_id,
                'name': d.name,
                'log_count': d.log_count,
            }
            for d in devices
        ]

        return Response(data)
