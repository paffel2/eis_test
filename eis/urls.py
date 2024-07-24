from django.urls import path
from .views import HouseViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"houses", HouseViewSet, "houses")


urlpatterns = router.urls
