from django.urls import path

from .views.reactions import create_comment, toggle_vote
from .views.suggestions import (
    change_status,
    create_suggestion,
    index,
    one_suggestion,
    profile,
    deletar_sugestao,
    editar_sugestao,
)

urlpatterns = [
    path("", index, name="index"),
    path("suggestions/create/", create_suggestion, name="create_suggestion"),
    path("profile/", profile, name="profile"),
    path("<int:suggestion_id>/", one_suggestion, name="one_suggestion"),
    path("<int:suggestion_id>/toggle_vote/", toggle_vote, name="toggle_vote"),
    path("<int:suggestion_id>/comment/", create_comment, name="create_comment"),
    path("<int:suggestion_id>/change_status/", change_status, name="change_status"),
    path('deletar/<int:suggestion_id>/', deletar_sugestao, name='deletar_sugestao'),
    path("<int:suggestion_id>/edit/", editar_sugestao, name="editar_sugestao"),
]
