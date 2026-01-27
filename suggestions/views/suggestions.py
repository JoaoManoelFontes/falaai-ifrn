from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, ExpressionWrapper, F, FloatField, OuterRef
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render

from suggestions.enums import SuggestionOrdenationTypes
from suggestions.forms import CommentForm, SuggestionForm
from suggestions.models import Category, Suggestion


@login_required(login_url="auth")
def profile(request):
    """Página de perfil do usuário com suas sugestões."""

    user_customer = request.user.customer

    user_voted = Suggestion.votes.through.objects.filter(
        suggestion_id=OuterRef("pk"), customer_id=user_customer.id
    )

    suggestions = (
        Suggestion.objects.filter(customer=user_customer)
        .only(
            "id",
            "title",
            "status",
            "description",
            "votes_count",
            "comments_count",
            "created_at",
            "category__name",
        )
        .select_related("category")
        .annotate(user_voted=Exists(user_voted))
    )

    ordenation_type = request.GET.get("ordenation", SuggestionOrdenationTypes.DEFAULT)
    category_id = request.GET.get("category")
    status = request.GET.get("status")

    if ordenation_type == SuggestionOrdenationTypes.FEATURED:
        suggestions = suggestions.annotate(
            featured_score=ExpressionWrapper(
                (Coalesce(F("votes_count"), 0) + Coalesce(F("comments_count"), 0))
                / 2.0,
                output_field=FloatField(),
            )
        ).order_by("-featured_score", "-created_at")

    elif ordenation_type == SuggestionOrdenationTypes.MOST_VOTED:
        suggestions = suggestions.order_by("-votes_count", "-created_at")

    else:
        ordenation_type = SuggestionOrdenationTypes.DEFAULT
        suggestions = suggestions.order_by("-created_at")

    if category_id and category_id != "":
        category_id = int(category_id)
        suggestions = suggestions.filter(category_id=category_id)

    if status and status != "":
        suggestions = suggestions.filter(status=status)

    return render(
        request,
        "profile.html",
        {
            "customer": user_customer,
            "suggestions": suggestions,
            "ordenation_type": ordenation_type,
            "ordenation_types": SuggestionOrdenationTypes.choices,
            "category": category_id,
            "categories": Category.objects.all().only("id", "name"),
            "status_types": Suggestion.Status.choices,
            "status": status,
        },
    )


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
        .exclude(status=Suggestion.Status.IMPLEMENTED)
    )

    ordenation_type = request.GET.get("ordenation", SuggestionOrdenationTypes.DEFAULT)
    category_id = request.GET.get("category")
    status = request.GET.get("status")

    if ordenation_type == SuggestionOrdenationTypes.FEATURED:
        suggestions = suggestions.annotate(
            featured_score=ExpressionWrapper(
                (Coalesce(F("votes_count"), 0) + Coalesce(F("comments_count"), 0))
                / 2.0,
                output_field=FloatField(),
            )
        ).order_by("-featured_score", "-created_at")

    elif ordenation_type == SuggestionOrdenationTypes.MOST_VOTED:
        suggestions = suggestions.order_by("-votes_count", "-created_at")

    else:
        ordenation_type = SuggestionOrdenationTypes.DEFAULT
        suggestions = suggestions.order_by("-created_at")

    if category_id and category_id != "":
        category_id = int(category_id)
        suggestions = suggestions.filter(category_id=category_id)

    if status and status != "":
        suggestions = suggestions.filter(status=status)

    return render(
        request,
        "index.html",
        {
            "suggestions": suggestions,
            "ordenation_type": ordenation_type,
            "ordenation_types": SuggestionOrdenationTypes.choices,
            "category": category_id,
            "categories": Category.objects.all().only("id", "name"),
            "status_types": Suggestion.Status.choices,
            "status": status,
        },
    )


def create_suggestion(request):
    """Página para criar uma nova sugestão."""

    if request.user.customer.isStaff:
        messages.error(request, "Apenas estudantes podem criar sugestões.")
        return redirect("index")

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


def one_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(
        Suggestion.objects.select_related("category", "customer", "customer__user"),
        pk=suggestion_id,
    )

    user_voted = False
    if request.user.is_authenticated:
        user_voted = suggestion.votes.filter(id=request.user.customer.id).exists()

    suggestion.user_voted = user_voted

    # Buscar comentários relacionados
    comments = suggestion.comments.select_related(
        "customer", "customer__user"
    ).order_by("-created_at")

    # Formulário de comentário
    comment_form = CommentForm()

    context = {
        "suggestion": suggestion,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "one_suggestion.html", context)


@login_required(login_url="auth")
def change_status(request, suggestion_id):
    """Altera o status de uma sugestão. Apenas staff pode fazer isso."""
    if request.method != "POST":
        return redirect("one_suggestion", suggestion_id=suggestion_id)

    # Verificar se o usuário é staff
    if not request.user.customer.isStaff:
        messages.error(request, "Você não tem permissão para alterar o status.")
        return redirect("one_suggestion", suggestion_id=suggestion_id)

    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    new_status = request.POST.get("status")

    # Validar o status
    valid_statuses = [choice[0] for choice in Suggestion.Status.choices]
    if new_status not in valid_statuses:
        messages.error(request, "Status inválido.")
        return redirect("one_suggestion", suggestion_id=suggestion_id)

    suggestion.status = new_status
    suggestion.save(update_fields=["status"])
    messages.success(
        request, f"Status alterado para: {suggestion.get_status_display()}"
    )

    return redirect("one_suggestion", suggestion_id=suggestion_id)


@login_required(login_url="auth")
def deletar_sugestao(request, suggestion_id):
    sugestao = get_object_or_404(Suggestion, id=suggestion_id)

    if request.method == "POST":
        sugestao.delete()
        return redirect("profile")


@login_required(login_url="auth")
def editar_sugestao(request, suggestion_id):
    sugestao = get_object_or_404(Suggestion, id=suggestion_id)

    if request.method == "POST":
        form = SuggestionForm(request.POST, instance=sugestao)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = SuggestionForm(instance=sugestao)

    return render(request, "edit.html", {"form": form, "suggestion": sugestao})
