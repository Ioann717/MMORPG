from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.http import HttpResponse

from allauth.account.views import SignupView

import random

from .forms import ConfirmCodeForm
from .models import Profile
from board.models import Author


# Границы диапазона для генерации кода подтверждения
MIN_LIMIT = 1000
MAX_LIMIT = 9999


class CustomSignupView(SignupView):
    def form_valid(self, form):
        custom_form_valid = super().form_valid(form)
        # Создание профиля и кода
        user = self.request.user
        code = random.randint(MIN_LIMIT, MAX_LIMIT)
        mail = user.email
        profile = Profile.objects.create(user_link=user, code=code)
        # Отправка письма с кодом
        html_content = render_to_string(
            'mail_confirmation.html',
            {
                'code': code,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Код подтверждения от MMORPG',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[mail]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return redirect('/accounts/confirm/')


class ConfirmFormView(FormView):
    model = Profile
    form_class = ConfirmCodeForm
    template_name = 'confirm_code.html'
    success_url = '/accounts/login/'
    context_object_name = 'profile_code'

    def form_valid(self, form):
        user = self.request.user
        valid_code = Profile.objects.get(user_link=user).code
        code = form.cleaned_data['code']
        if code == valid_code:
            # Создание автора, добавление его в группы с правами создания/редактирования постов
            Author.objects.create(user_link=user, status=True)
            post_makers = Group.objects.get(name="post makers")
            user.groups.add(post_makers)
            comment_makers = Group.objects.get(name="comment makers")
            user.groups.add(comment_makers)
            # Удаление объекта профиля с кодом, чтоб избежать повторение кодов
            Profile.objects.get(user_link=user).delete()
            return super().form_valid(form)
        else:
            message = 'Введен неверный код!'
            return HttpResponse(message)
