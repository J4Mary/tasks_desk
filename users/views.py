from django.contrib.auth import login
from django.contrib.auth import logout as logout_
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.views.generic import ListView

from users import models
from users.forms import RegisterForm
from users.models import User


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('/')
    return render(request, 'users/register.html', {'form': form})


def logout(request):
    logout_(request)
    return redirect('/')


class UserListView(ListView):
    model = models.User

    def post(self, request, *args, **kwargs):
        new_user_id = request.POST.get('user_id')
        new_user = models.User.objects.get(pk=new_user_id)
        action = request.POST.get('action')
        if action == 'approve':
            new_user.active = True
            new_user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

