from rest_framework.serializers import Serializer, CharField, ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField
from users.models import User
from .models import Company


class CompanyDataSerializer(Serializer):
    nome = CharField(max_length=255, required=True, allow_blank=True)
    fantasia = CharField(max_length=255, required=True, allow_blank=True)
    status = CharField(max_length=100, required=True, allow_blank=True)

    def validate(self, data):
        data['legal_name'] = data.pop('nome', None) 
        data['brand_name'] = data.pop('fantasia', None)
        data = {key: value for key, value in data.items() if value is not None and value != ''}
        return data
    
    class Meta:
        model = Company
        fields = ['brand_name', 'legal_name', 'status']

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
