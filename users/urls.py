from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import UserListView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('new_users', UserListView.as_view(), name='new_users'),

]