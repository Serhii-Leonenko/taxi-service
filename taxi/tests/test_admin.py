from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="Admin12345"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="Driver12345",
            license_number="TES12345"
        )

    def test_driver_license_listed(self):
        """Tests that driver's license is in list_display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_listed(self):
        """Tests that driver's license is in driver detail page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_add_license_listed(self):
        """Tests that field license_number is in driver add page"""
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, "License number")
