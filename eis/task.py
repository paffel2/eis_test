from datetime import timedelta, date

from celery import shared_task

from .models import (
    House,
    ApartmentBill,
    Rate,
)
from .serializers import CounterReadingListSerializer


# @shared_task
def calculate_bills(house_id, current_date):
    house = House.objects.get(id=house_id)
    rates = Rate.objects.all()
    result = []
    for apartment in house.apartments.all():
        household_rate = [x for x in rates if x.rate_type == "HOUSEHOLD"][0]
        total_bill = household_rate.price * apartment.area
        apartment_bill = ApartmentBill(
            apartment=apartment, date=current_date, total_bill=0
        )
        for counter in apartment.counters.all():
            current_value = (
                counter.readings.all()
                .filter(date__year=current_date.year, date__month=current_date.month)
                .first()
            )

            previous_month = date(
                year=current_date.year, month=current_date.month, day=1
            ) - timedelta(days=1)

            previous_value = counter.readings.filter(
                date__year=previous_month.year, date__month=previous_month.month
            ).first()

            print(f"{current_value=}")

            delta = current_value.reading
            if previous_value:
                delta = delta - previous_value.reading
            rate = [x for x in rates if x.rate_type == counter.rate_type][0]
            bill = delta * rate.price
            total_bill += bill
            current_value.bill = bill
            current_value.save()
        apartment_bill.total_bill = total_bill
        apartment_bill.save()
        result.append(apartment_bill)
    print(result)
    return result
