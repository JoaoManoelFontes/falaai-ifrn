from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "isStaff",
        "course",
        "profile_img_url",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "matricula",
        "cpf",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Informações do Usuário", {"fields": ("user", "matricula", "cpf", "role")}),
        ("Contato e Perfil", {"fields": ("phone_number", "profile_img_url")}),
        (
            "Datas de Registro",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
