from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import StudentOnboarding
from datetime import date

class StudentOnboardingModelTest(TestCase):
    def setUp(self):
        self.student_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': date(2005, 6, 15),
            'gender': 'M',
            'email': 'john.doe@example.com',
            'mobile_number': '+1234567890',
            'address_line_1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'country': 'United States',
            'zipcode': '10001',
            'citizenship': 'US',
            'guardian_name': 'Jane Doe',
            'guardian_relationship': 'Mother',
            'guardian_phone': '+1234567891',
            'guardian_email': 'jane.doe@example.com',
            'father_name': 'Robert Doe',
            'father_profession': 'engineer',
            'mother_name': 'Jane Doe',
            'mother_profession': 'teacher',
            'family_income': '75000.00',
            'number_of_siblings': 2,
            'has_family_abroad': False,
        }

    def test_create_student_onboarding(self):
        """Test creating a student onboarding record"""
        student = StudentOnboarding.objects.create(**self.student_data)
        self.assertEqual(student.first_name, 'John')
        self.assertEqual(student.last_name, 'Doe')
        self.assertEqual(student.email, 'john.doe@example.com')

    def test_student_string_representation(self):
        """Test the string representation of the model"""
        student = StudentOnboarding.objects.create(**self.student_data)
        expected = "John Doe - john.doe@example.com"
        self.assertEqual(str(student), expected)

class StudentOnboardingAPITest(APITestCase):
    def setUp(self):
        self.create_url = reverse('student-onboarding-create')
        self.dropdown_url = reverse('dropdown-options')
        
        self.valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2005-06-15',
            'gender': 'M',
            'email': 'john.doe@example.com',
            'mobile_number': '+1234567890',
            'address_line_1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'country': 'United States',
            'zipcode': '10001',
            'citizenship': 'US',
            'guardian_name': 'Jane Doe',
            'guardian_relationship': 'Mother',
            'guardian_phone': '+1234567891',
            'guardian_email': 'jane.doe@example.com',
            'father_name': 'Robert Doe',
            'father_profession': 'engineer',
            'mother_name': 'Jane Doe',
            'mother_profession': 'teacher',
            'family_income': '75000.00',
            'number_of_siblings': 2,
            'has_family_abroad': False,
        }

    def test_create_student_onboarding_success(self):
        """Test successful creation of student onboarding"""
        response = self.client.post(self.create_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('student_id', response.data)
        self.assertIn('data', response.data)

    def test_create_student_onboarding_invalid_email(self):
        """Test creation with invalid email"""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_create_student_onboarding_invalid_phone(self):
        """Test creation with invalid phone number"""
        invalid_data = self.valid_data.copy()
        invalid_data['mobile_number'] = 'invalid-phone'
        response = self.client.post(self.create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('mobile_number', response.data)

    def test_get_dropdown_options(self):
        """Test getting dropdown options"""
        response = self.client.get(self.dropdown_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('gender', response.data)
        self.assertIn('citizenship', response.data)
        self.assertIn('countries', response.data)
        self.assertIn('states', response.data)
        self.assertIn('professions', response.data)

    def test_get_student_detail(self):
        """Test getting student detail"""
        # First create a student
        create_response = self.client.post(self.create_url, self.valid_data, format='json')
        student_id = create_response.data['student_id']
        
        # Then get the student detail
        detail_url = reverse('student-onboarding-detail', kwargs={'student_id': student_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_update_student(self):
        """Test updating student information"""
        # First create a student
        create_response = self.client.post(self.create_url, self.valid_data, format='json')
        student_id = create_response.data['student_id']
        
        # Then update the student
        update_url = reverse('student-onboarding-update', kwargs={'student_id': student_id})
        update_data = {
            'mobile_number': '+1234567899',
            'family_income': '80000.00'
        }
        response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['data']['mobile_number'], '+1234567899')
        self.assertEqual(response.data['data']['family_income'], '80000.00') 