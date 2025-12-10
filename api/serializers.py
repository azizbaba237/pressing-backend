from rest_framework import serializers
from .models import Service, Order, OrderItem, Customer, Payment
from django.contrib.auth.models import User
from django.utils import timezone



def validate_progress_percent(value):
    if not (0 <= value <= 100):
        raise serializers.ValidationError("progress_percent doit être entre 0 et 100")
    return value

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        write_only=True,
        source="service"
    )

    class Meta:
        model = OrderItem
        fields = ("id", "service", "service_id", "quantity", "price")
        extra_kwargs = {
            'price': {'required': False}  # Rendre le champ price optionnel
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        write_only=True,
        source="customer"
    )

    class Meta:
        model = Order
        fields = ("id", "customer_id", "created_at", "due_date", "status", "total", "items", "notes",
                  "progress_percent")
        read_only_fields = ("total", "created_at")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items_data:
            svc = item["service"]
            # Utiliser le prix fourni ou celui du service par défaut
            price = item.get("price", svc.price)
            quantity = item.get("quantity", 1)
            OrderItem.objects.create(order=order, service=svc, quantity=quantity, price=price)
            total += price * quantity
        order.total = total
        order.save()
        return order

    def update(self, instance, validated_data):
        # Gérer update status / items selon les besoins
        items_data = validated_data.pop("items", None)

        # Mettre à jour les champs de base
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Si des items sont fournis, les mettre à jour
        if items_data is not None:
            # Supprimer les anciens items
            instance.items.all().delete()

            # Créer les nouveaux items
            total = 0
            for item in items_data:
                svc = item["service"]
                price = item.get("price", svc.price)
                quantity = item.get("quantity", 1)
                OrderItem.objects.create(order=instance, service=svc, quantity=quantity, price=price)
                total += price * quantity
            instance.total = total

        instance.save()
        return instance

    progress_percent = serializers.IntegerField(validators=[validate_progress_percent], required=False)

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("due_date doit être une date future")
        return value


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Customer
        fields = ("id", "username", "email", "phone", "address")