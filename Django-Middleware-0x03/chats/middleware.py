from datetime import datetime
import logging

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