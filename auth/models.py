import uuid

from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    ROLE_CHOICES = [
        ("aluno", "Aluno"),
        ("staff", "Staff"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    matricula = models.CharField(max_length=14, unique=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="aluno")
    profile_img_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "customers"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-created_at"]
