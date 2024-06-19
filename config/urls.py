from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui",),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc",),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
