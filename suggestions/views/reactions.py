from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

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
