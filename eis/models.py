from django.db import models


class RateType(models.TextChoices):
    HOT_WATER = "HOT_WATER"
    COLD_WATER = "COLD_WATER"
    HOUSEHOLD = "HOUSEHOLD"


class ProcessStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class House(models.Model):
    address = models.CharField(max_length=250, unique=True)


class Apartment(models.Model):
    number = models.IntegerField()
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="apartments"
    )
    area = models.DecimalField(max_digits=5, decimal_places=2)


class Rate(models.Model):
    rate_type = models.CharField(max_length=10, choices=RateType, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Counter(models.Model):
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name="counters"
    )
    rate_type = models.CharField(max_length=10, choices=RateType)

    class Meta:
        unique_together = (
            "apartment",
            "rate_type",
        )


class CounterReading(models.Model):
    counter = models.ForeignKey(
        Counter, on_delete=models.CASCADE, related_name="readings"
    )
    reading = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    bill = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class ApartmentBill(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    date = models.DateField()
    total_bill = models.DecimalField(max_digits=10, decimal_places=2)


class BillProcess(models.Model):
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="bill_processes"
    )
    status = models.CharField(
        max_length=11, choices=ProcessStatus, default="IN_PROGRESS"
    )
    date = models.DateField()

    class Meta:
        unique_together = (
            "house",
            "date",
        )
