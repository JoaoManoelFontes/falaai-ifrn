from django.urls import path

from auth.views import auth, logout_view

urlpatterns = [
    path(
        "",
        auth,
        name="auth",
    ),
    path(
        "logout/",
        logout_view,
        name="logout",
    ),
]
