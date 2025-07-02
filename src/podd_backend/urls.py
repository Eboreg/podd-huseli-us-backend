from django.urls import include, path


urlpatterns = [
    path("", include("spodcat.urls")),
    path("admin/", include("spodcat.contrib.admin.urls")),
]

try:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
except ImportError:
    pass
