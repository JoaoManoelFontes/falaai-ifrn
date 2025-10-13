from django.urls import path

from .views.suggestions import index

urlpatterns = [
    path("", index, name="index"),
]
