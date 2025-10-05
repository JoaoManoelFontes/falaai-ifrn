from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="auth")
def index(request):
    """Página inicial das sugestões."""
    return render(request, "index.html")
