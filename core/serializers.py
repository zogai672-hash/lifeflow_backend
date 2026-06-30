from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Donor, BloodInventory, BloodRequest, DonationRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DonorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        allow_null=True,
        default=None
    )

    class Meta:
        model = Donor
        fields = [
            'id', 'user', 'first_name', 'last_name',
            'blood_type', 'date_of_birth', 'phone',
            'email', 'location', 'address', 'weight',
            'medical_notes', 'status', 'date_registered'
        ]


class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = [
            'id', 'blood_type', 'units_available',
            'minimum_threshold', 'last_updated'
        ]


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = [
            'id', 'requester_name', 'hospital',
            'blood_type', 'units_needed', 'priority',
            'status', 'notes', 'date_requested'
        ]


class DonationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRecord
        fields = [
            'id', 'donor', 'blood_type', 'units',
            'transaction_type', 'notes', 'date'
        ]
        extra_kwargs = {
            'donor': {'required': False, 'allow_null': True}
        }