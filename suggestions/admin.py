from django.contrib import admin

from .models import Category, Comment, Media, Suggestion


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1
    fields = ["file"]
    verbose_name = "Mídia"
    verbose_name_plural = "Mídias"


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ["customer", "text", "created_at"]
    readonly_fields = ["created_at"]
    verbose_name = "Comentário"
    verbose_name_plural = "Comentários"


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "customer",
        "category",
        "status",
        "votes_count",
        "comments_count",
        "created_at",
    )
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "customer__name")
    readonly_fields = ("created_at", "updated_at", "votes_count", "comments_count")
    inlines = [MediaInline, CommentInline]
    ordering = ("-created_at",)
    list_per_page = 20

    fieldsets = (
        (
            "Informações principais",
            {
                "fields": ("title", "description", "customer", "category", "status"),
            },
        ),
        (
            "Engajamento",
            {
                "fields": ("votes_count", "comments_count"),
            },
        ),
        (
            "Datas",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("customer", "category")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text_short", "customer", "suggestion", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text", "customer__name", "suggestion__title")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 30

    def text_short(self, obj):
        return (obj.text[:60] + "...") if len(obj.text) > 60 else obj.text

    text_short.short_description = "Texto"


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("file_name", "suggestion")
    search_fields = ("file", "suggestion__title")
    ordering = ("suggestion",)
    list_per_page = 20

    def file_name(self, obj):
        return obj.file.name.split("/")[-1]

    file_name.short_description = "Arquivo"
