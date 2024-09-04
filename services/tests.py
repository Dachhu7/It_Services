from django.test import TestCase
from .models import Service

class ServiceModelTests(TestCase):
    def test_string_representation(self):
        service = Service(name="Test Service")
        self.assertEqual(str(service), "Test Service")

    def test_service_creation(self):
        service = Service.objects.create(
            name="Test Service",
            payment_terms="Monthly",
            price=100.00,
            package="Basic Package",
            tax=10.00,
            image=None
        )
        self.assertEqual(service.name, "Test Service")
        self.assertEqual(service.price, 100.00)