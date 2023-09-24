from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment, Author


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Поле 'author' передается через form_valid в представлении
        fields = [
            'title',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 5:
            raise ValidationError({
                "title": "Заголовок объявления не может быть менее 5 символов."
            })
        text = cleaned_data.get("text")
        if text is not None and len(text) < 15:
            raise ValidationError({
                "text": "Текст объявления не может быть менее 15 символов."
            })
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Поля 'author' и 'post' передается через form_valid в представлении
        fields = [
            'text',
        ]
