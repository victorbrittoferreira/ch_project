from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField
from users.models import User
from .models import Company

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'tax_number', 'brand_name', 'legal_name']

    def create(self, validated_data):
        return super().create(validated_data)
    
class CompanyMemberSerializer(ModelSerializer):
    members = PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=True)

    class Meta:
        model = Company
        fields = ['members']

    def update(self, instance: Company, validated_data):
        member_ids = validated_data.get('members')
        instance.members.add(*member_ids)
        return instance


class MembersSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'full_name']

    def get_full_name(self, obj: User):
        return f"{obj.first_name} {obj.last_name}"
