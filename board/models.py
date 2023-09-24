from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    status = models.BooleanField(default=False)
    user_link = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_link.username}'


class Post(models.Model):
    tanks = 'ta'
    heals = 'he'
    dd = 'dd'
    traders = 'tr'
    guildmasters = 'gm'
    questgivers = 'gq'
    blacksmiths = 'bs'
    tanners = 'tn'
    potionmasters = 'pm'
    spellmasters = 'sm'

    CATEGORY_CHOICE = [
        (tanks, 'Танки'),
        (heals, 'Хилы'),
        (dd, 'ДД'),
        (traders, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potionmasters, 'Зельевары'),
        (spellmasters, 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=55)
    text = RichTextUploadingField()
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICE, default=tanks)
    time_add = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}: {self.text[:50]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    text = models.TextField(max_length=10000)
    time_add = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} --> От {self.author.user_link.username}: {self.text[:50]}'
