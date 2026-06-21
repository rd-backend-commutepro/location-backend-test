from django.urls import path
from .views import (
    LocationUpdateView,
    LocationHistoryView,
    HealthCheckView,
    CreateSuperUserView,   # ← add this
)

urlpatterns = [
    path('location/update/', LocationUpdateView.as_view()),
    path('location/history/', LocationHistoryView.as_view()),
    path('health/', HealthCheckView.as_view()),
    path('create-superuser/', CreateSuperUserView.as_view()),  # ← add this
]
