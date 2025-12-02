from django.test import TestCase
from Registration.forms import NewUserRegistrationForm
from Registration.view_address import DIVISION_LIST, GEOGRAPHY_DATA


class RegistrationFormTests(TestCase):
	def test_form_invalid_when_required_missing(self):
		# Missing password & gender should make it invalid
		data = {
			'full_name': 'Test Student',
			'email': 'test@example.com',
			'phone': '01234567890',
			'dob': '2008-01-01',
			'school_name': 'Test School',
			'student_class': '6',
			'division': 'Dhaka',
			'district': 'Dhaka',
			'upazila': 'Dhamrai'
		}
		form = NewUserRegistrationForm(data)
		self.assertFalse(form.is_valid())
		self.assertIn('password', form.errors)
		self.assertIn('confirm_password', form.errors)
		self.assertIn('gender', form.errors)

	def test_form_valid_when_all_fields_and_choices_provided(self):
		data = {
			'full_name': 'Test Student',
			'email': 'test@example.com',
			'phone': '01234567890',
			'dob': '2008-01-01',
			'school_name': 'Test School',
			'student_class': '6',
			'division': 'Dhaka',
			'district': 'Dhaka',
			'upazila': 'Dhamrai',
			'password': 'supersecret',
			'confirm_password': 'supersecret',
			'gender': 'Male'
		}

		form = NewUserRegistrationForm(data)
		# emulate view logic: set choices from address lookup
		form.fields['division'].choices = [('', '-- Select Division --')] + [(d,d) for d in DIVISION_LIST]
		form.fields['district'].choices = [('', '-- Select District --')] + [(d,d) for d in list(GEOGRAPHY_DATA['Dhaka'].keys())]
		form.fields['upazila'].choices = [('', '-- Select Upazila --')] + [(u,u) for u in GEOGRAPHY_DATA['Dhaka']['Dhaka']]

		self.assertTrue(form.is_valid())
