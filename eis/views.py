from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ApartmentSerializer,
    ApartmentBillSerializer,
    RateSerializer,
    HouseSerializer,
    CounterSerializer,
    CounterReadingSerializer,
)
from .models import (
    House,
    Apartment,
    Counter,
    CounterReading,
    ApartmentBill,
    Rate,
)


class HouseViewSet(ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
