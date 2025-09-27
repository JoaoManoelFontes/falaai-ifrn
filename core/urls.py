from django.contrib import admin
from django.urls import include, path

from auth.urls import urlpatterns as auth_urls

from .views import index_view

urlpatterns = [
    path("", index_view, name="index"),
    path("auth/", include(auth_urls)),
    path("admin/", admin.site.urls),
]
