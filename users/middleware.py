from time import time
from django.contrib.auth import logout
from requests import session

from helpdesk.settings import SESSION_TIMEOUT


class LogoutUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        last_activity = request.session.get('last_activity')
        now = time()
        idle = now - last_activity if last_activity else 0

        if idle > SESSION_TIMEOUT:
            logout(session)
        else:
            request.session['last_activity'] = now
            response = self.get_response(request)
            return response
