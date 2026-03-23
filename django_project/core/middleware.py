"""
core/middleware.py — Custom Django Middleware
"""
import time
import logging

logger = logging.getLogger('trendpulse')


class RequestLoggingMiddleware:
    """Logs every request: method, path, status, duration."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        t0 = time.time()
        response = self.get_response(request)
        ms = (time.time() - t0) * 1000
        logger.info('%s %s %d (%.0fms)', request.method, request.path, response.status_code, ms)
        return response
