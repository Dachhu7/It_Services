from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    payment_terms = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    # image = models.ImageField(upload_to='services/')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription for {self.service.name} at {self.address}"