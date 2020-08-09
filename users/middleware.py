import time
from django.contrib.auth import logout

SESSION_TIMEOUT = 300


class HandleSessionExpiryMiddleware(object):
    def process_request(self, request):
        last_activity = request.session.get('last_activity')
        now = time.time()
        idle = now - last_activity if last_activity else 0

        timeout = SESSION_TIMEOUT

        if idle > timeout:
            pass
            #run_on_expiry()
            #logout(session)
        else:

            request.session['last_activity'] = now
            idle = 0
