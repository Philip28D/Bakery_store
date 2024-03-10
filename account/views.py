from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import RegisterForm
from django.http import HttpResponseRedirect


class LoginView(AuthLoginView):
    template_name = 'account/login.html'


class LogoutView(AuthLogoutView):
    def get_next_page(self):
        # user logout before redirect
        logout(self.request)
        return HttpResponseRedirect(reverse('app_bakerystore:home'))


def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('app_bakerystore:home'))  # home-page redirect
    return render(request, 'account/register.html', {'form': form})
