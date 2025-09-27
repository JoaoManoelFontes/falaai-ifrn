from django.urls import path

from auth.views import auth_form_view

urlpatterns = [
    path(
        "",
        auth_form_view,
        name="auth",
    ),
]
