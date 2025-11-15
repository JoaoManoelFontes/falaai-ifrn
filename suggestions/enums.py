from django.db import models


class SuggestionOrdenationTypes(models.TextChoices):
    DEFAULT = "default", "Mais recentes"
    FEATURED = "featured", "Em destaque"
    MOST_VOTED = "most_voted", "Mais votadas"
