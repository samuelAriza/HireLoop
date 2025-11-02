"""
Middleware personalizado para health checks
"""

class HealthCheckMiddleware:
    """
    Middleware que permite health checks desde cualquier host sin redirecciones HTTPS.
    Debe estar ANTES de SecurityMiddleware en MIDDLEWARE.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.health_check_paths = ['/health/', '/ready/', '/healthz/']

    def __call__(self, request):
        # Si es un health check, bypassear validaciones de seguridad
        if request.path in self.health_check_paths:
            # Marcar como conexión segura para evitar redirect HTTPS
            request._secure_override = True
            request.META['wsgi.url_scheme'] = 'https'
            
        response = self.get_response(request)
        return response