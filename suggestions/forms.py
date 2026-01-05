from django import forms

from suggestions.models import Comment, Suggestion


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ["title", "description", "category"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent",
                    "placeholder": "Digite o título da sua sugestão",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none",
                    "placeholder": "Conte-nos sobre sua ideia: qual problema ela resolve? Como pode ser"
                    " implementada? Quais são os benefícios esperados?",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control w-full px-4 py-2 rounded-lg border border-gray-300 bg-white focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise forms.ValidationError("O título precisa conter 5 ou mais caracteres.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 20:
            raise forms.ValidationError(
                "A descrição precisa conter 20 ou mais caracteres."
            )
        return description


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border-2 px-4 py-2 rounded-md mb-4 outline-none focus:border-green-600",
                    "placeholder": "Adicione um comentário...",
                }
            ),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text")
        if not text or len(text.strip()) < 3:
            raise forms.ValidationError(
                "O comentário precisa conter pelo menos 3 caracteres."
            )
        return text.strip()
