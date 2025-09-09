from rest_framework import serializers
from .models import UserAccount
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import UserAccount

class UserAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'first_name', 'last_name', 'email', 'address',
            'phone_number', 'whatsapp_number', 'date_of_birth',
            'national_id_number', 'citizenship', 'country_of_residence',
            'profile_pic', 'cover_photo', 'company_name', 'category'
        ]

    def validate(self, data):
        # Ensure artist fields are validated only for artists
        if self.instance.is_agent:
            if 'company_name' in data and not data['company_name']:
                raise serializers.ValidationError("Stage name cannot be empty.")
            if 'category' in data and not data['category']:
                raise serializers.ValidationError("category cannot be empty.")
        return data

class CustomUserSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = UserAccount
        fields ='__all__'
        read_only_fields = ('id', 'is_superuser', 'is_staff', 'is_agent', 'is_dealer', 'date_joined')
    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.is_agent:
            return 'agent'
        elif obj.is_dealer:
            return 'dealer'
        return 'individual'