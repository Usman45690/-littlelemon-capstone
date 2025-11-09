from django.test import TestCase
from django.contrib.auth.models import User
from .models import Menu, Booking

class MenuModelTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            name="Test Menu Item",
            price=10.99,
            description="Test description"
        )

    def test_menu_creation(self):
        self.assertEqual(self.menu.name, "Test Menu Item")
        self.assertEqual(self.menu.price, 10.99)

class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="John",
            reservation_date="2025-12-25",
            reservation_slot=18
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, "John")
        self.assertEqual(self.booking.reservation_slot, 18)

class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_api_access(self):
        response = self.client.get('/api/menus/')
        self.assertEqual(response.status_code, 200)