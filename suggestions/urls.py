from django.urls import path

from .views.reactions import toggle_vote
from .views.suggestions import create_suggestion, index, one_suggestion, profile

urlpatterns = [
    path("", index, name="index"),
    path("suggestions/create/", create_suggestion, name="create_suggestion"),
    path("profile/", profile, name="profile"),
    path("<int:suggestion_id>/", one_suggestion, name="one_suggestion"),
    path("<int:suggestion_id>/toggle_vote/", toggle_vote, name="toggle_vote"),
]
