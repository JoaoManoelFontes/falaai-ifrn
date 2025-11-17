from django.urls import path

from .views.suggestions import create_suggestion, index, one_suggestion

urlpatterns = [
    path("", index, name="index"),
    path("suggestions/create/", create_suggestion, name="create_suggestion"),
    path("<int:suggestion_id>/", one_suggestion, name='one_suggestion'),
]
