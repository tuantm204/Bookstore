from rest_framework import serializers
from .models import Customer


class AddressSerializer(serializers.Serializer):
    """Serializer cho Address (nested representation)"""
    street = serializers.CharField(max_length=500, required=False, allow_blank=True)
    city = serializers.CharField(max_length=255, required=False, allow_blank=True)
    state = serializers.CharField(max_length=255, required=False, allow_blank=True)
    zip_code = serializers.CharField(max_length=20, required=False, allow_blank=True)


class CustomerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    full_address = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'email', 'phone', 'job',
            'street', 'city', 'state', 'zip_code',
            'address', 'full_address',
            'created_at', 'updated_at'
        ]

    def get_address(self, obj):
        return {
            'street': obj.street or '',
            'city': obj.city or '',
            'state': obj.state or '',
            'zip_code': obj.zip_code or '',
        }


class CustomerCreateSerializer(serializers.ModelSerializer):
    """Serializer cho tạo/cập nhật Customer"""

    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'email', 'phone', 'job',
            'street', 'city', 'state', 'zip_code',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_email(self, value):
        # Check unique khi tạo mới
        if self.instance is None:
            if Customer.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email đã tồn tại.")
        else:
            if Customer.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email đã tồn tại.")
        return value


class UpdateCustomerSerializer(serializers.ModelSerializer):
    """Serializer cho cập nhật Customer - tất cả fields optional"""

    class Meta:
        model = Customer
        fields = [
            'full_name', 'email', 'phone', 'job',
            'street', 'city', 'state', 'zip_code',
        ]
        extra_kwargs = {
            'full_name': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'job': {'required': False},
            'street': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
            'zip_code': {'required': False},
        }

    def validate_email(self, value):
        if self.instance and Customer.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Email đã tồn tại.")
        return value
