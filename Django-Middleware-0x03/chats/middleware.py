from datetime import datetime, timedelta
import logging
from django.http import HttpResponseForbidden

# Configure a logger for requests
logger = logging.getLogger('request_logger')
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user info - if not authenticated, use 'AnonymousUser'
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        
        # Log the datetime, user, and request path
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response
    class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}  # key: IP, value: list of datetime objects

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = datetime.now()

        if request.method == 'POST':
            timestamps = self.message_log.get(ip, [])
            # Remove timestamps older than 1 minute
            timestamps = [ts for ts in timestamps if now - ts < timedelta(minutes=1)]
            if len(timestamps) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")
            timestamps.append(now)
            self.message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        # This handles common headers in production setups behind proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')