from django.contrib import messages
from django.shortcuts import render

from auth.clients.suap import SuapClient
from auth.exceptions import SuapAPIError, SuapAuthError


def auth(request):
    """View para autenticação e cadastro de usuários via SUAP."""
    if request.method == "POST":
        suap_client = SuapClient()

        matricula = request.POST.get("matricula")
        senha = request.POST.get("senha")

        try:
            token = suap_client.authenticate(matricula, senha)
            print("Token:", token)
            messages.success(request, "Login realizado com sucesso!")

            return render(request, "index.html")
        except SuapAuthError:
            messages.error(request, "Matrícula ou senha incorretos.")
        except SuapAPIError as e:
            messages.error(request, f"Ocorreu um erro ao conectar ao SUAP: {e}")

    return render(request, "auth/form.html")
