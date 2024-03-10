from django.urls import path
from .views import LoginView, register, LogoutView


app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]