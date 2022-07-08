from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormsTest(TestCase):
    def test_driver_creating_form_with_first_last_name_and_license(self):
        form_data = {
            "username": "test_user",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "Test name",
            "last_name": "Test last name",
            "license_number": "TES12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_license_form_not_valid_short_password(self):
        form_data = {
            "license_number": "TES1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_not_valid_lowercase_password(self):
        form_data = {
            "license_number": "TeS1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_update_license_form_not_valid_not_enough_decimals_password(self):
        form_data = {
            "license_number": "TESS1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
