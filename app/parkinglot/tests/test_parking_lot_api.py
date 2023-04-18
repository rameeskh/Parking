"""
Test for parkinglot APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import ParkingLot
from parkinglot.serializers import ParkingLotSerializer


PARKINGLOT_URL = reverse('parkinglot:parkinglot-list')


def detail_url(parkinglot_id):
    """Create and return a recipe detail URL."""
    return reverse('parkinglot:parkinglot-detail', args=[parkinglot_id])


def create_parkinglot(user, **params):
    """Create and return a sample parkinglot"""
    defaults = {
        'name': 'Sample parkinglot Title',
        'address': 'Street Address'
    }
    defaults.update(params)

    parkinglot = ParkingLot.objects.create_parking_lot(user=user, **defaults)
    return parkinglot


def create_superuser(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicParkingLotApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required to call APIs"""
        res = self.client.get(PARKINGLOT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateParkingApiTests(TestCase):
    """Test for authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_superuser(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_parkinglots(self):
        """Test retrieving a list of parkinglots"""
        create_parkinglot(user=self.user)
        create_parkinglot(user=self.user)

        res = self.client.get(PARKINGLOT_URL)

        parkinglots = ParkingLot.objects.all()
        serializer = ParkingLotSerializer(parkinglots, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_parkinglot_detail(self):
        """Test get parkinglot detail"""
        parkinglot = create_parkinglot(user=self.user)
        
        url = detail_url(parkinglot.id)
        res = self.client.get(url)

        serializer = ParkingLotSerializer(parkinglot)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_parkinglot(self):
        """Test partial update of parkinglot"""
        parkinglot = create_parkinglot(user=self.user)

        payload = {
            'name': 'Updated name',
        }
        url = detail_url(parkinglot.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        parkinglot.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(parkinglot, k), v)
        self.assertEqual(parkinglot.user, self.user)

    def test_full_update_parkinglot(self):
        """Test for full update of parkinglot"""
        parkinglot = create_parkinglot(user=self.user)
        
        payload = {
            'name': "Updated name",
            'address': 'Updated address'
        }
        url = detail_url(parkinglot.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        parkinglot.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(parkinglot, k), v)
        self.assertEqual(parkinglot.user, self.user)

    def test_delete_parkinglot(self):
        """Test deletion of parkinglot api"""
        parkinglot = create_parkinglot(user=self.user)

        url = detail_url(parkinglot.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ParkingLot.objects.filter(id=parkinglot.id).exists())
