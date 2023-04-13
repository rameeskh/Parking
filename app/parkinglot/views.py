"""
Views for Parkinglot APIs
"""
from core.models import (
    ParkingLot,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from parkinglot import serializers


class ParkingLotViewSet(viewsets.ModelViewSet):
    """View for managing Parkinglot APIs."""
    serializer_class = serializers.ParkingLotSerializer
    queryset = ParkingLot.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
