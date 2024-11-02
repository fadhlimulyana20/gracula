from django.urls import path
from .views import index, SendEmailView

urlpatterns = [
    path('', index, name='index'),
    path('send-email/', SendEmailView.as_view(), name='send-email'),
]