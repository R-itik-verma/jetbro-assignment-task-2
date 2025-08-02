from django.urls import path
from .views import (
    StudentOnboardingListView,
    StudentOnboardingCreateView,
    StudentOnboardingDetailView,
    StudentOnboardingUpdateView,
    get_dropdown_options,
    api_documentation
)

urlpatterns = [
    path('', api_documentation, name='api-docs'),
    path('student-onboarding/', StudentOnboardingListView.as_view(), name='student-onboarding-list'),
    path('student-onboarding/create/', StudentOnboardingCreateView.as_view(), name='student-onboarding-create'),
    path('student-onboarding/<int:student_id>/', StudentOnboardingDetailView.as_view(), name='student-onboarding-detail'),
    path('student-onboarding/<int:student_id>/update/', StudentOnboardingUpdateView.as_view(), name='student-onboarding-update'),
    path('dropdown-options/', get_dropdown_options, name='dropdown-options'),
] 