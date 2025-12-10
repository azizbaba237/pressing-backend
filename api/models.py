from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(default=60)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending","Pending"),
        ("in_progress","In Progress"),
        ("ready","Ready"),
        ("delivered","Delivered"),
        ("cancelled","Cancelled"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_orders")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    progress_percent = models.IntegerField(default=0)  # 0-100
    notes = models.TextField(blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of price

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)  # cash, card, mobile money
    reference = models.CharField(max_length=200, blank=True, null=True)

