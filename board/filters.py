from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post, Comment, Author


class CommentFilter(FilterSet):
    # Для организации поиска по объявлениям
    post = ModelMultipleChoiceFilter(
        field_name='post',
        queryset=Post.objects.all(),
        label='Объявления',
        conjoined=False,  # поиск по принципу ИЛИ
    )
