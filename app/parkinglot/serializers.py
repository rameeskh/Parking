"""
Serializers for parkinglot api
"""
from rest_framework import serializers

from core.models import (
    ParkingLot
)


class ParkingLotSerializer(serializers.ModelSerializer):
    """Serializer for Parkinglots"""

    class Meta:
        model = ParkingLot
        fields = ['id', 'name', 'address']

    def create(self, validated_data):
        if not validated_data.get('user').is_superuser:
            raise serializers.ValidationError("Admin can only create")
        return ParkingLot.objects.create_parking_lot(**validated_data)
