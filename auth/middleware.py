from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class CustomerRequiredMiddleware:
    """
    Impede o acesso de usuários sem Customer vinculado à aplicação.
    Exceto em:
      - páginas de login
      - páginas do admin
      - arquivos estáticos
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        exempt_paths = [
            reverse("auth"),
            reverse("admin:index"),
        ]

        if (
            user.is_authenticated
            and not hasattr(user, "customer")
            and not any(request.path.startswith(path) for path in exempt_paths)
            and not request.path.startswith("/admin/")
            and not request.path.startswith("/static/")
        ):
            messages.error(
                request, "Acesso negado: seu usuário não possui um perfil ativo."
            )
            return redirect("auth")

        return self.get_response(request)
