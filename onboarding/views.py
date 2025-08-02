from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from django.shortcuts import get_object_or_404, render
from .models import StudentOnboarding
from .serializers import StudentOnboardingSerializer, StudentOnboardingListSerializer

class StudentOnboardingListView(ListAPIView):
    """List all student onboarding records"""
    queryset = StudentOnboarding.objects.all().order_by('-created_at')
    serializer_class = StudentOnboardingListSerializer

class StudentOnboardingCreateView(CreateAPIView):
    """Create a new student onboarding record"""
    queryset = StudentOnboarding.objects.all()
    serializer_class = StudentOnboardingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                'message': 'Student onboarding created successfully',
                'student_id': student.id,
                'data': StudentOnboardingSerializer(student).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentOnboardingDetailView(RetrieveAPIView):
    """Retrieve a specific student onboarding record"""
    queryset = StudentOnboarding.objects.all()
    serializer_class = StudentOnboardingSerializer
    lookup_field = 'student_id'
    
    def get_object(self):
        return get_object_or_404(StudentOnboarding, id=self.kwargs['student_id'])

class StudentOnboardingUpdateView(UpdateAPIView):
    """Update a specific student onboarding record"""
    queryset = StudentOnboarding.objects.all()
    serializer_class = StudentOnboardingSerializer
    lookup_field = 'student_id'
    
    def get_object(self):
        return get_object_or_404(StudentOnboarding, id=self.kwargs['student_id'])
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                'message': 'Student onboarding updated successfully',
                'data': StudentOnboardingSerializer(student).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_dropdown_options(request):
    """Get dropdown options for various fields (CMS simulation)"""
    options = {
        'gender': [
            {'value': 'M', 'label': 'Male'},
            {'value': 'F', 'label': 'Female'},
            {'value': 'O', 'label': 'Other'},
        ],
        'citizenship': [
            {'value': 'US', 'label': 'United States'},
            {'value': 'CA', 'label': 'Canada'},
            {'value': 'UK', 'label': 'United Kingdom'},
            {'value': 'IN', 'label': 'India'},
            {'value': 'AU', 'label': 'Australia'},
            {'value': 'OTHER', 'label': 'Other'},
        ],
        'countries': [
            {'value': 'US', 'label': 'United States'},
            {'value': 'CA', 'label': 'Canada'},
            {'value': 'UK', 'label': 'United Kingdom'},
            {'value': 'IN', 'label': 'India'},
            {'value': 'AU', 'label': 'Australia'},
            {'value': 'DE', 'label': 'Germany'},
            {'value': 'FR', 'label': 'France'},
            {'value': 'JP', 'label': 'Japan'},
        ],
        'states': [
            {'value': 'CA', 'label': 'California'},
            {'value': 'NY', 'label': 'New York'},
            {'value': 'TX', 'label': 'Texas'},
            {'value': 'FL', 'label': 'Florida'},
            {'value': 'IL', 'label': 'Illinois'},
        ],
        'professions': [
            {'value': 'engineer', 'label': 'Engineer'},
            {'value': 'doctor', 'label': 'Doctor'},
            {'value': 'teacher', 'label': 'Teacher'},
            {'value': 'lawyer', 'label': 'Lawyer'},
            {'value': 'business', 'label': 'Business'},
            {'value': 'other', 'label': 'Other'},
        ]
    }
    
    return Response(options)

@api_view(['GET'])
def api_documentation(request):
    """Serve API documentation HTML page"""
    return render(request, 'onboarding/api_docs.html') 