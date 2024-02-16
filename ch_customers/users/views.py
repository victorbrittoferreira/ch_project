from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

