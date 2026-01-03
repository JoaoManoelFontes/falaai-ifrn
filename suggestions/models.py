from django.db import models, transaction


class Suggestion(models.Model):
    class Status(models.TextChoices):
        ANALYSE = "ANALYSE", "Em análise"
        IMPLEMENTATION = "IMPLEMENTATION", "Em implementação"
        IMPLEMENTED = "IMPLEMENTED", "Implementada"

    title = models.CharField(max_length=255)
    description = models.TextField()
    customer = models.ForeignKey("project_auth.Customer", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=None,
        null=True,
        blank=True,
    )
    votes_count = models.IntegerField(default=0)
    votes = models.ManyToManyField(
        "project_auth.Customer", related_name="voted_suggestions", blank=True
    )
    comments_count = models.IntegerField(default=0)
    category = models.ForeignKey(
        "suggestions.Category", on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "suggestions"
        verbose_name = "Sugestão"
        verbose_name_plural = "Sugestões"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title

    @transaction.atomic
    def toggle_vote(self, customer) -> bool:
        """
        Alterna o voto do customer:
        - Se já votou: remove o voto (desvotar)
        - Se não votou: adiciona o voto (votar)
        """

        if self.votes.filter(id=customer.id).exists():
            self.votes.remove(customer)
            self.votes_count = models.F("votes_count") - 1
            voted = False
        else:
            self.votes.add(customer)
            self.votes_count = models.F("votes_count") + 1
            voted = True

        self.save(update_fields=["votes_count"])
        self.refresh_from_db(fields=["votes_count"])

        return voted


class Media(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    file = models.FileField(upload_to="suggestions/")

    class Meta:
        db_table = "medias"
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"

    def __str__(self):
        return self.file.name


class Comment(models.Model):
    customer = models.ForeignKey("project_auth.Customer", on_delete=models.CASCADE)
    suggestion = models.ForeignKey("suggestions.Suggestion", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name
