from django.shortcuts import render


def auth_form_view(request):
    if request.method == "POST":
        matricula = request.POST.get("matricula")
        senha = request.POST.get("senha")

        print(matricula, senha)

    return render(request, "auth/form.html")
