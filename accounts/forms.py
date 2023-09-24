from django.contrib.auth.models import Group
from django import forms

from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm): # Для добавления в основные группы при регистрации на сайте
    def save(self, request):
        user = super().save(request)
        # post_makers = Group.objects.get(name="post makers")
        # user.groups.add(post_makers)
        # comment_makers = Group.objects.get(name="comment makers")
        # user.groups.add(comment_makers)
        return user


class ConfirmCodeForm(forms.Form):
    code = forms.IntegerField()
