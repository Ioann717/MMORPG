from celery import shared_task
import time
import datetime

from django.conf import settings

from board.models import Author, Post

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Отправка рассылки с объявлениями за неделю
@shared_task
def mail_for_authors():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_add__gte=last_week)
    authors = set(Author.objects.all().values_list('user_link__email', flat=True))
    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Объявления за прошедшую неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=authors,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
