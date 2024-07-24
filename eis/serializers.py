from rest_framework import serializers
from .models import (
    House,
    Apartment,
    Counter,
    CounterReading,
    ApartmentBill,
    Rate,
)


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = "__all__"


class CounterReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterReading
        fields = "__all__"


class ApartmentBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentBill
        fields = "__all__"
