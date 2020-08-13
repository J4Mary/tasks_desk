from time import time

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
# from requests import session

from django.conf import settings


class LogoutUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        last_activity = request.session.get('last_activity')
        now = time()
        idle = now - last_activity if last_activity else 0

        if idle > settings.SESSION_TIMEOUT:
            logout(request)
            messages.success(request, "You did nothing for so long! Please, sign in again")
            return redirect('/')
        else:
            request.session['last_activity'] = now
            response = self.get_response(request)
            return response
