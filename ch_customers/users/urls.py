from django.urls import path
from .views import  UserCreateAPIView

urlpatterns = [
    path('user/', UserCreateAPIView.as_view(), name='create_user'),
]
