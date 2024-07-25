from django.urls import path, include


from .views import (
    CountersViewSet,
    HouseViewSet,
    ApartmentsViewSet,
    RateViewSet,
    CounterReadingsViewSet,
)
from rest_framework_nested import routers


house_router = routers.SimpleRouter()
house_router.register(r"houses", HouseViewSet, "houses")

apartment_router = routers.NestedSimpleRouter(house_router, r"houses", lookup="house")
apartment_router.register(r"apartments", ApartmentsViewSet, basename="house-apartments")

counter_router = routers.NestedSimpleRouter(
    apartment_router, r"apartments", lookup="apartment"
)
counter_router.register(r"counters", CountersViewSet, basename="apartment-counters")

rates_router = routers.SimpleRouter()
rates_router.register(r"rates", RateViewSet)

counter_readings_router = routers.NestedSimpleRouter(
    counter_router, r"counters", lookup="counter"
)

counter_readings_router.register(
    r"readings", CounterReadingsViewSet, basename="counter-readings"
)


urlpatterns = [
    path("", include(house_router.urls)),
    path("", include(apartment_router.urls)),
    path("", include(counter_router.urls)),
    path("", include(rates_router.urls)),
    path("", include(counter_readings_router.urls)),
]
