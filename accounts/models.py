from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user_link = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.PositiveSmallIntegerField(default=1111)

    def __str__(self):
        return f'{self.user_link.username}'