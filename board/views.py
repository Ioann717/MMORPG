from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Post, Comment, Author
from .forms import PostForm, CommentForm
from .filters import CommentFilter

# Для вывода доски объявлений
class PostsList(ListView):
    model = Post
    ordering = 'time_add'
    template_name = 'board.html'
    context_object_name = 'posts'
    paginate_by = 7

    # Вывод названий категории
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.model.CATEGORY_CHOICE
        return context

 # Вывод отдельных категорий
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# Создание обьявлений с проверкой прав
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

# Редактирование объявления с проверкой прав
class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

# Удаление объявления с проверкой прав
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

# Вывод откликов
class CommentList(ListView):
    model = Comment
    ordering = 'time_add'
    template_name = 'responses.html'
    context_object_name = 'comments'

    # Оставляем только отклики на объявления текущего пользователя
    def get_queryset(self):
        queryset = Comment.objects.filter(post__author__user_link__pk=self.request.user.pk)
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# Создание отклика с проверкой прав
class CommentCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_comment',)
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        form.instance.author = self.request.user.author
        post = form.instance.post
        mail = Author.objects.get(post=post).user_link.email
        html_content = render_to_string(
            'mail_new_comment.html',
            {
                'post': post.title,
                'link': f'{settings.SITE_URL}/board/responses'
            }
        )
        msg = EmailMultiAlternatives(
            subject='Новый отклик на ваше объявление',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[mail]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return super().form_valid(form)

# Удаление отклика с проверкой прав
class CommentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_comment',)
    model = Comment
    context_object_name = 'comment'
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('comment_list')

# Вывод отдельных откликов
class CommentDetail(DetailView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'


# Функция-представления одобрения
@login_required()
def approve(request, **kwargs):
    comment = Comment.objects.get(pk=kwargs['pk'])
    comment.approval = True
    comment.save()
    # Отправка оповещения автору
    post = comment.post
    mail = comment.author.user_link.email
    html_content = render_to_string(
        'mail_response_approved.html',
        {
            'post': post.title,
            'link': f'{settings.SITE_URL}/board/{ post.id }'
        }
    )
    msg = EmailMultiAlternatives(
        subject='Ваш отклик был принят!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[mail]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return redirect('../../')
