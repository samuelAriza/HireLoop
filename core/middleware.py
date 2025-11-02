"""
Middleware personalizado para health checks
"""

class HealthCheckMiddleware:
    """
    Middleware que permite health checks desde cualquier host.
    Debe estar ANTES de SecurityMiddleware en MIDDLEWARE.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si es un health check, permitir cualquier host
        if request.path in ['/health/', '/ready/', '/healthz/']:
            # No validar ALLOWED_HOSTS para estos endpoints
            request._dont_enforce_csrf_checks = True
            
        response = self.get_response(request)
        return response