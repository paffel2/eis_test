import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from django.db.utils import IntegrityError
from .serializers import (
    ApartmentSerializer,
    ApartmentListSerializer,
    ApartmentBillSerializer,
    RateSerializer,
    HouseSerializer,
    HouseListSerializer,
    CounterSerializer,
    CounterReadingSerializer,
    CounterReadingListSerializer,
)
from .models import (
    House,
    Apartment,
    Counter,
    CounterReading,
    ApartmentBill,
    Rate,
)
from .task import calculate_bills


class CRUDViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ["get", "post", "delete", "put"]


class HouseViewSet(CRUDViewSet):
    queryset = House.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return HouseListSerializer
        else:
            return HouseSerializer


class ApartmentsViewSet(CRUDViewSet):
    queryset = Apartment.objects.all().select_related("house")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ApartmentListSerializer
        else:
            return ApartmentSerializer

    def create(self, request, house_pk: int):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        number = serializer.validated_data["number"]
        area = serializer.validated_data["area"]
        house = House.objects.get(pk=house_pk)
        apartment = Apartment(number=number, area=area, house=house)
        apartment.save()
        result = ApartmentSerializer(apartment)
        return Response(result.data, status=201)


class CountersViewSet(CRUDViewSet):
    queryset = Counter.objects.all().select_related("apartment")
    serializer_class = CounterSerializer

    def create(self, request, apartment_pk: int, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rate_type = serializer.validated_data["rate_type"]
        if rate_type == "HOUSEHOLD":
            return Response({"message": "this counter type doesn't exist"}, status=400)
        apartment = Apartment.objects.get(pk=apartment_pk)
        counter = Counter(apartment=apartment, rate_type=rate_type)
        try:
            counter.save()
        except IntegrityError:
            return Response({"message": "counter already exist"}, status=400)
        result = CounterSerializer(counter)
        return Response(result.data, status=201)


class RateViewSet(CRUDViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class CounterReadingsViewSet(CRUDViewSet):
    queryset = CounterReading.objects.all().select_related("counter")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CounterReadingListSerializer
        else:
            return CounterReadingSerializer

    def create(self, request, counter_pk: int, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reading = serializer.validated_data["reading"]
        counter = Counter.objects.get(id=counter_pk)
        counter_reading = CounterReading(counter=counter, reading=reading)
        counter_reading.save()
        result = CounterReadingListSerializer(counter_reading)
        return Response(result.data, status=201)


class TestView(viewsets.GenericViewSet):
    queryset = Rate.objects.all()

    def list(self, request):
        result = calculate_bills(1, datetime.date(year=2024, month=7, day=1))
        answer = []
        for i in result:
            answer.append(ApartmentBillSerializer(i).data)
        return Response(answer, status=200)
