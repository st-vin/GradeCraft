from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from .models import CustomUser

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


class HomePageView(TemplateView):
    template_name = 'registration/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/dashboard.html'


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SignupView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # Redirect after successful signup

    def form_valid(self, form):
        response = super().form_valid(form)
        # Ensure CSRF cookie is set
        self.request.META["CSRF_COOKIE_USED"] = True
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect after logout

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/dashboard.html'
    

