from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    tax_number = models.CharField(max_length=14, unique=True)
    brand_name = models.CharField(max_length=100, unique=True)
    legal_name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_companies')
    members = models.ManyToManyField(User, related_name='member_companies')
