"""
URL mapping of the parkinglot
"""
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

from parkinglot import views


router = DefaultRouter()
router.register('parkinglots', views.ParkingLotViewSet)

app_name = 'parkinglot'

urlpatterns = [
    path('', include(router.urls)),
]
