from django.contrib import admin
from .models import StudentOnboarding

@admin.register(StudentOnboarding)
class StudentOnboardingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile_number', 'created_at')
    list_filter = ('gender', 'citizenship', 'has_family_abroad', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'mobile_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'mobile_number')
        }),
        ('Address Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'zipcode', 'citizenship')
        }),
        ('Family Information', {
            'fields': ('guardian_name', 'guardian_relationship', 'guardian_phone', 'guardian_email')
        }),
        ('Family Details', {
            'fields': ('father_name', 'father_profession', 'mother_name', 'mother_profession')
        }),
        ('Financial Information', {
            'fields': ('family_income',)
        }),
        ('Additional Information', {
            'fields': ('number_of_siblings', 'has_family_abroad', 'countries_abroad')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 