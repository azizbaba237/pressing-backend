from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, OrderViewSet, CustomerViewSet
router = DefaultRouter()
router.register("services", ServiceViewSet)
router.register("orders", OrderViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
  path("", include(router.urls)),
]
