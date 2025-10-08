from django.contrib import admin
from django.urls import include, path

from auth.urls import urlpatterns as auth_urls
from suggestions.urls import urlpatterns as suggestions_urls

urlpatterns = [
    path("", include(suggestions_urls)),
    path("auth/", include(auth_urls)),
    path("admin/", admin.site.urls),
]
