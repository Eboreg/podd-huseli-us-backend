from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView


urlpatterns: list = [
    path("", include("spodcat.urls")),
    path("admin/", include("spodcat.contrib.admin.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain; charset=utf-8")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

try:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
except ImportError:
    pass
