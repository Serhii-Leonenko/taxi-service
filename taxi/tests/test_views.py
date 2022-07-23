from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Test12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="test1",
            country="test_country1"
        )
        Manufacturer.objects.create(
            name="test2",
            country="test_country2"
        )

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverCreateTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverCreateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="new_user",
            password="Test12345"
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_user",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "Test name",
            "last_name": "Test last name",
            "license_number": "TES12345"
        }

        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicCarCreateTests(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_CREATE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarCreateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="new_user",
            password="Test12345"
        )
        self.client.force_login(self.user)

    def test_create_car(self):

        manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="japan"
        )

        form_data = {
            "model": "car_model",
            "manufacturer": manufacturer.id,
            "drivers": [f"{self.user.id}", ]
        }

        self.client.post(CAR_CREATE_URL, data=form_data)
        new_car = Car.objects.get(model="car_model")

        self.assertEqual(new_car.model, form_data["model"])
        self.assertEqual(new_car.manufacturer.id, form_data["manufacturer"])
        self.assertIn(int(form_data["drivers"][0]), new_car.drivers.all().values_list("id", flat=True))


class TestCarDeleteAddDriverView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="new_user",
            password="Test12345"
        )
        self.client.force_login(self.user)

    def test_car_delete_driver(self):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="japan"
        )
        car = Car.objects.create(
            model="car",
            manufacturer=manufacturer
        )
        car.drivers.add(self.user)
        url = reverse("taxi:car-detail", kwargs={'pk': car.id})
        res = self.client.get(url)
        self.assertContains(res, "Delete me from this car")

    def test_car_add_driver(self):
        manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="japan"
        )
        car = Car.objects.create(
            model="car",
            manufacturer=manufacturer
        )
        url = reverse("taxi:car-detail", kwargs={'pk': car.id})
        res = self.client.get(url)
        self.assertContains(res, "Assign me to this car")
