from django.urls import path

from .views.suggestions import create_suggestion, index, profile

urlpatterns = [
    path("", index, name="index"),
    path("suggestions/create/", create_suggestion, name="create_suggestion"),
    path("profile/", profile, name="profile"),
]
