from rest_framework import viewsets
from .models import Service, Order, Customer
from .serializers import ServiceSerializer, OrderSerializer, CustomerSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("customer")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        # client sees uniquement ses commandes
        customer = getattr(user, "customer_profile", None)
        if customer:
            return Order.objects.filter(customer=customer)
        return Order.objects.none()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
