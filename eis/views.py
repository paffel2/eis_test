import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY
from .serializers import (
    ApartmentSerializer,
    ApartmentListSerializer,
    ApartmentBillSerializer,
    BillProcessSerializer,
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
    BillProcess,
)
from .task import calculate_bills_task


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

    @action(detail=True, methods=["GET"])
    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "year",
                IN_QUERY,
                type="int",
            ),
            Parameter("month", IN_QUERY, type="int"),
        ],
    )
    def calculate_bills(self, request, pk: int):

        year_str = request.GET.get("year")
        month_str = request.GET.get("month")
        if not year_str or not month_str:
            return Response({"error": "No year and month parameters"}, status=400)
        try:
            year = int(year_str)
            month = int(month_str)
        except ValueError:
            return Response(
                {"error": "Bad format of year and month parameters"}, status=400
            )
        house = House.objects.get(id=pk)
        date = datetime.date(year=year, month=month, day=1)
        calculation_task = BillProcess(house=house, date=date)
        calculation_task.save()
        calculate_bills_task.delay(pk, date)
        bill_process_serializers = BillProcessSerializer(calculation_task)
        return Response(bill_process_serializers.data, status=201)

    @action(detail=True, methods=["GET"])
    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "year",
                IN_QUERY,
                type="int",
            ),
            Parameter("month", IN_QUERY, type="int"),
        ],
    )
    def get_bills(self, request, pk: int, *args, **kwargs):
        year_str = request.GET.get("year")
        month_str = request.GET.get("month")
        if not year_str or not month_str:
            return Response({"error": "No year and month parameters"}, status=400)
        try:
            year = int(year_str)
            month = int(month_str)
        except ValueError:
            return Response(
                {"error": "Bad format of year and month parameters"}, status=400
            )
        date = datetime.date(year=year, month=month, day=1)
        apartment_bill = ApartmentBillSerializer(
            data=ApartmentBill.objects.filter(apartment__house__id=pk, date=date),
            many=True,
        )
        apartment_bill.is_valid()
        return Response(apartment_bill.data, status=200)

    @action(detail=True, methods=["GET"])
    def get_bill_process(self, request, pk: int, *args, **kwargs):
        processes = BillProcessSerializer(
            data=BillProcess.objects.filter(house__id=pk), many=True
        )
        processes.is_valid()
        return Response(processes.data, status=200)


class ApartmentsViewSet(CRUDViewSet):
    def get_queryset(self):
        return Apartment.objects.filter(house__id=self.kwargs["house_pk"])

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

    @action(detail=True, methods=["GET"])
    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                "year",
                IN_QUERY,
                type="int",
            ),
            Parameter("month", IN_QUERY, type="int"),
        ],
    )
    def get_bill(self, request, pk: int, *args, **kwargs):
        year_str = request.GET.get("year")
        month_str = request.GET.get("month")
        if not year_str or not month_str:
            return Response({"error": "No year and month parameters"}, status=400)
        try:
            year = int(year_str)
            month = int(month_str)
        except ValueError:
            return Response(
                {"error": "Bad format of year and month parameters"}, status=400
            )
        date = datetime.date(year=year, month=month, day=1)
        apartment_bill = ApartmentBillSerializer(
            ApartmentBill.objects.filter(apartment__id=pk, date=date).first()
        )
        return Response(apartment_bill.data, status=200)


class CountersViewSet(CRUDViewSet):
    def get_queryset(self):
        return Counter.objects.filter(apartment__id=self.kwargs["apartment_pk"])

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
    def get_queryset(self):
        return CounterReading.objects.filter(counter__id=self.kwargs["counter_pk"])

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
