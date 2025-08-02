from rest_framework import serializers
from .models import StudentOnboarding
from .validators import validate_phone_number, validate_email_format

class StudentOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOnboarding
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_email(self, value):
        return validate_email_format(value)
    
    def validate_mobile_number(self, value):
        return validate_phone_number(value)
    
    def validate_guardian_phone(self, value):
        return validate_phone_number(value)
    
    def validate(self, data):
        # Custom validation logic
        if data.get('date_of_birth'):
            from datetime import date
            today = date.today()
            age = today.year - data['date_of_birth'].year - (
                (today.month, today.day) < (data['date_of_birth'].month, data['date_of_birth'].day)
            )
            if age < 5 or age > 100:
                raise serializers.ValidationError("Age must be between 5 and 100 years")
        
        # Validate family income
        if data.get('family_income') and data['family_income'] < 0:
            raise serializers.ValidationError("Family income cannot be negative")
        
        return data

class StudentOnboardingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOnboarding
        fields = ['id', 'first_name', 'last_name', 'email', 'created_at'] 