import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (hour in 24h format)
        current_hour = datetime.datetime.now().hour

        # Restrict access if current time is NOT between 18:00 (6PM) and 21:00 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to the chat is only allowed between 6 PM and 9 PM.")

        # Otherwise continue processing the request
        response = self.get_response(request)
        return response