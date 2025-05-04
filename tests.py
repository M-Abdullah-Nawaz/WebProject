from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ContactUsAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('contact-us')  # The name you gave in urls.py
        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "subject": "Testing Subject",
            "message": "This is a test message from API testing."
        }
        self.invalid_payload = {
            "first_name": "",
            "last_name": "Doe",
            "email": "invalid-email",  # Invalid email format
            "phone": "1234567890",
            "subject": "",
            "message": ""
        }

    def test_contact_us_success(self):
        """Test ContactUs API with valid payload"""
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Your message has been sent successfully!')

    def test_contact_us_failure_invalid_email(self):
        """Test ContactUs API with invalid payload (invalid email)"""
        response = self.client.post(self.url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_contact_us_failure_missing_fields(self):
        """Test ContactUs API when required fields are missing"""
        response = self.client.post(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('message', response.data)
