# from django.urls import path, include

# urlpatterns = [
#     path("restaurants", include("restaurants.urls")),
#     path("users", include("users.urls")),
# ]

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view( 
    openapi.Info( 
        title="Panomix", 
        default_version="v1", 
        description="Panomix program API documentation", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="jihoon", email="jihoon@gmail.com"), 
        license=openapi.License(name="Panomix.io"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
    path("", include("restaurants.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        ]