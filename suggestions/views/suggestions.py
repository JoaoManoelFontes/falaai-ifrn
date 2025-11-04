from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import redirect, render

from suggestions.forms import SuggestionForm
from suggestions.models import Suggestion


@login_required(login_url="auth")
def index(request):
    """Página inicial das sugestões."""

    user_customer = request.user.customer

    user_voted = Suggestion.votes.through.objects.filter(
        suggestion_id=OuterRef("pk"), customer_id=user_customer.id
    )

    suggestions = (
        Suggestion.objects.all()
        .only(
            "id",
            "title",
            "status",
            "description",
            "votes_count",
            "comments_count",
            "created_at",
            "category__name",
            "customer__user__first_name",
            "customer__profile_img_url",
        )
        .select_related("category", "customer", "customer__user")
        .annotate(user_voted=Exists(user_voted))
        .order_by("-created_at")
        .exclude(status=Suggestion.Status.IMPLEMENTED)
    )

    return render(request, "index.html", {"suggestions": suggestions})


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
