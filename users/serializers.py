from rest_framework import serializers
from .models import UserAccount
from djoser.serializers import UserSerializer as BaseUserSerializer

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
        # Ensure agent fields are validated only for agents
        if self.instance and self.instance.is_agent:
            if 'company_name' in data and not data.get('company_name'):
                raise serializers.ValidationError("Company name cannot be empty for an agent.")
            if 'category' in data and not data.get('category'):
                raise serializers.ValidationError("Category cannot be empty for an agent.")
        return data

class CustomUserSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = UserAccount
        fields = '__all__' # Using all fields from the model
        read_only_fields = ('id', 'is_superuser', 'is_staff', 'is_agent', 'is_dealer', 'date_joined')
    
    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.is_agent:
            return 'agent'
        elif obj.is_dealer:
            return 'dealer'
        return 'individual'

