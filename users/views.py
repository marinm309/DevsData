from django.views import generic as views
from . forms import CustomAuthenticationForm, SignUpForm, CustomerForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Customer
from django.contrib.messages.views import SuccessMessageMixin


UserModel = get_user_model()

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    success_message = 'Login successful!'
    


class UserCreationView(SuccessMessageMixin, views.CreateView):
    template_name = 'users/register.html'
    form_class = SignUpForm
    success_url=reverse_lazy('home')
    success_message = 'Account created successfuly!'

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    
class UserLogoutView(LogoutView):
    pass
