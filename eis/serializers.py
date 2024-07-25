from rest_framework import serializers
from .models import (
    House,
    Apartment,
    Counter,
    CounterReading,
    ApartmentBill,
    Rate,
    BillProcess,
)


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = ["id", "rate_type"]


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ["id", "number", "area"]


class ApartmentListSerializer(serializers.ModelSerializer):
    counters = CounterSerializer(many=True)

    class Meta:
        model = Apartment
        fields = "__all__"


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"


class HouseListSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True)

    class Meta:
        model = House
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class CounterReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterReading
        fields = ["reading"]


class CounterReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterReading
        fields = "__all__"


class ApartmentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentBill
        fields = "__all__"


class BillProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillProcess
        fields = "__all__"
