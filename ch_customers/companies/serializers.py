from rest_framework import serializers

from users.models import User
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'tax_number', 'brand_name', 'legal_name']

    def create(self, validated_data):
        return super().create(validated_data)