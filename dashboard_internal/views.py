from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Protected dashboard — redirects to admin login if not authenticated.
    LoginRequiredMixin uses LOGIN_URL which defaults to /accounts/login/
    We override it to use the admin login instead.
    """
    template_name = 'dashboard_internal/index.html'
    login_url = '/admin/login/'
