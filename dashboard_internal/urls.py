from django.urls import path
from .views import DashboardView

app_name = 'dashboard_internal'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]
