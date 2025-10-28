from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from suggestions.forms import SuggestionForm


@login_required(login_url="auth")
def index(request):
    """Página inicial das sugestões."""
    return render(request, "index.html")


def create_suggestion(request):
    """Página para criar uma nova sugestão."""

    if request.method == "POST":
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.customer = request.user.customer
            suggestion.save()
            messages.success(request, "Sugestão criada com sucesso!")
            return redirect("index")

        messages.error(request, "Por favor, corrija os erros abaixo.")

    form = SuggestionForm()
    return render(request, "suggestion_form.html", {"form": form})
