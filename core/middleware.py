from django.http import HttpResponse
import requests

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
    
class HttpCatMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:
            url = f"https://http.cat/{response.status_code}"
            r = requests.get(url)
            return HttpResponse(r.content, content_type="image/jpeg", status=response.status_code)
        return response