from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re

class StudentOnboarding(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    CITIZENSHIP_CHOICES = [
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        ('IN', 'India'),
        ('AU', 'Australia'),
        ('OTHER', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: +1234567890'
            )
        ]
    )
    
    # Address Information
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    citizenship = models.CharField(max_length=10, choices=CITIZENSHIP_CHOICES)
    
    # Family Information
    guardian_name = models.CharField(max_length=200)
    guardian_relationship = models.CharField(max_length=50)
    guardian_phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: +1234567890'
            )
        ]
    )
    guardian_email = models.EmailField()
    
    # Family Details
    father_name = models.CharField(max_length=200, blank=True, null=True)
    father_profession = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=200, blank=True, null=True)
    mother_profession = models.CharField(max_length=100, blank=True, null=True)
    
    # Financial Information
    family_income = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Additional Information
    number_of_siblings = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    has_family_abroad = models.BooleanField(default=False)
    countries_abroad = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_onboarding'
        verbose_name = 'Student Onboarding'
        verbose_name_plural = 'Student Onboardings'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    def clean(self):
        # Custom validation
        if self.family_income < 0:
            raise ValidationError('Family income cannot be negative')
        
        # Email domain validation (optional)
        if self.email and '@' in self.email:
            domain = self.email.split('@')[1]
            if len(domain) < 3:
                raise ValidationError('Invalid email domain')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs) 