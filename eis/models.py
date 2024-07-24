from django.db import models


class RateType(models.TextChoices):
    HOT_WATER = "HOT_WATER"
    COLD_WATER = "COLD_WATER"
    HOUSEHOLD = "HOUSEHOLD"


class House(models.Model):
    address = models.CharField(max_length=250, unique=True)


class Apartment(models.Model):
    number = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=5, decimal_places=2)


class Rate(models.Model):
    rate_type = models.CharField(max_length=10, choices=RateType)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Counter(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    rate_type = models.CharField(max_length=10, choices=RateType)


class CounterReading(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    reading = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    bill = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class ApartmentBill(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    date = models.DateField()
    total_bill = models.DecimalField(max_digits=10, decimal_places=2)
