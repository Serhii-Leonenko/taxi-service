from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_create_driver_with_license_and_str(self):
        username = "test"
        password = "Test12345"
        license_number = "TES12345"
        first_name = "Test_first_name"
        last_name = "Test_last_name"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name
        )

        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)
        self.assertEqual(
            str(driver), f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        self.assertEqual(str(manufacturer), f"{manufacturer.name} ({manufacturer.country})")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
