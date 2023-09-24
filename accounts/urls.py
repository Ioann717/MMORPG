from django.urls import path, include

from .views import CustomSignupView, ConfirmFormView


urlpatterns = [
    path('signup/', CustomSignupView.as_view()),
    path('confirm/', ConfirmFormView.as_view()),
    path('', include('allauth.urls')),
]
