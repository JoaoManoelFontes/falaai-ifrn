from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from auth.clients.suap import SuapClient
from auth.clients.suapUserDTO import SuapUserDTO
from auth.exceptions import SuapAPIError, SuapAuthError
from auth.models import Customer


def auth(request):
    """View para autenticação e cadastro de usuários via SUAP."""
    if request.method == "POST":
        suap_client = SuapClient()

        matricula = request.POST.get("matricula")
        senha = request.POST.get("senha")

        try:
            suap_client.authenticate(matricula, senha)

            suap_user = suap_client.get_user_data()
            suap_user.password = senha

            customer = get_or_register_customer(suap_user)
            login(request, customer.user)

            messages.success(request, "Login realizado com sucesso!")
            return redirect("index")
        except SuapAuthError:
            messages.error(request, "Matrícula ou senha incorretos.")
        except SuapAPIError as e:
            messages.error(request, f"Ocorreu um erro ao conectar ao SUAP: {e}")

    return render(request, "auth/form.html")


def get_or_register_customer(suapUserDTO: SuapUserDTO) -> Customer:
    """
    Obtém ou registra um cliente com base nos dados do usuário SUAP.

    Args:
        suapUserDTO (SuapUserDTO): DTO com os dados do usuário SUAP.

    Returns:
        Customer: Cliente registrado ou existente.
    """
    existent_customer = Customer.objects.filter(
        user__username=suapUserDTO.registry
    ).first()

    if existent_customer:
        return existent_customer

    user = User.objects.create_user(
        username=suapUserDTO.registry,
        first_name=suapUserDTO.name,
        password=suapUserDTO.password,
        email=suapUserDTO.email,
    )

    return Customer.objects.create(
        user=user,
        isStaff=suapUserDTO.role == SuapUserDTO.Role.STAFF,
        profile_img_url=suapUserDTO.profile_img_url,
        course=suapUserDTO.course,
    )


def logout_view(request):
    """Desloga o usuário e redireciona para a página de login."""
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect("auth")
