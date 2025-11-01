from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def root_health_check(request):
    return JsonResponse({"status": "ok"}, status=200)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls", namespace="core")),
    path("", include("microservices.urls", namespace="microservices")),
    path("projects/", include("projects.urls", namespace="projects")),
    path(
        "mentorship_sessions/",
        include("mentorship_session.urls", namespace="mentorship_session"),
    ),
    path("cart/", include("cart.urls", namespace="cart")),
    path("payments/", include("payments.urls", namespace="payment")),
    path("analytics/", include("analytics.urls", namespace="analytics")),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path("api/", include("microservices.api.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    path("", root_health_check, name="root_health_check"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
