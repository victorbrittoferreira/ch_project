from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


def days_forward():
    days = 30
    return timezone.now().date() + timedelta(days=days)

class Company(models.Model):
    tax_number = models.CharField(RegexValidator(r'^\d{14}$'), unique=True)
    brand_name = models.CharField(max_length=100, unique=True)
    legal_name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_companies')
    members = models.ManyToManyField(User, related_name='member_companies')
    status = models.CharField(max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    next_update_rf = models.DateField(default=days_forward) 
