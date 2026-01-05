from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from suggestions.forms import CommentForm
from suggestions.models import Suggestion


@login_required
def toggle_vote(request, suggestion_id):
    if request.method != "POST":
        return redirect("home")

    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    customer = request.user.customer

    suggestion.toggle_vote(customer)

    referer = request.META.get("HTTP_REFERER", "")
    if referer:
        return redirect(f"{referer.split('#')[0]}#suggestion-{suggestion_id}")
    return redirect("home")


@login_required
def create_comment(request, suggestion_id):
    """Cria um novo comentário para uma sugestão."""
    if request.method != "POST":
        return redirect("one_suggestion", suggestion_id=suggestion_id)

    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    customer = request.user.customer

    form = CommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data["text"]
        suggestion.add_comment(customer, text)
        messages.success(request, "Comentário adicionado com sucesso!")
    else:
        messages.error(request, "Por favor, corrija os erros no comentário.")

    referer = request.META.get("HTTP_REFERER", "")
    if referer:
        return redirect(f"{referer.split('#')[0]}#comments")
    return redirect("one_suggestion", suggestion_id=suggestion_id)
