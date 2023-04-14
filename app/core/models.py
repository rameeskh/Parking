"""
Database Models
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import PermissionDenied


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, password):
        """create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ParkingLotManager(models.Manager):
    """Manager for parkinglot model"""
    def create_parking_lot(self, name, address, user):
        """create and return the parkinglot instance"""
        if not user.is_superuser:
            raise PermissionDenied(
                "Only admin users can create ParkingLot objects."
                )
        parkinglot = self.create(name=name, address=address, user=user)
        return parkinglot


class ParkingLot(models.Model):
    """ParkingLot in the system."""
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    objects = ParkingLotManager()

    def __str__(self):
        return self.name


class Spot(models.Model):
    """spot in the parkinglot"""
    spot_types = [
        ('BIKE', 'Bike'),
        ('CAR', 'Car'),
        ('OTHERS', 'Others')
    ]
    spot_type = models.CharField(max_length=50, choices=spot_types, default='CAR')
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='spot')
    occupied = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.pk
