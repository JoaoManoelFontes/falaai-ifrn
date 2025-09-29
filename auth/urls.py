from django.urls import path

from auth.views import auth

urlpatterns = [
    path(
        "",
        auth,
        name="auth",
    ),
]
