# ==================== PROJECT STRUCTURE ====================
# hospital_appointment/
# ├── manage.py
# ├── requirements.txt
# ├── hospital_appointment/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   └── wsgi.py
# └── appointments/
#     ├── __init__.py
#     ├── models.py
#     ├── serializers.py
#     ├── views.py
#     ├── urls.py
#     └── admin.py

# ==================== requirements.txt ====================
"""
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
psycopg2-binary==2.9.9
python-decouple==3.8
djangorestframework-simplejwt==5.3.0
Pillow==10.1.0
"""

# ==================== hospital_appointment/settings.py ====================
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'appointments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospital_appointment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospital_appointment.wsgi.application'

# Database - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hospital_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# For MySQL, use:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hospital_db',
#         'USER': 'root',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Change in production
CORS_ALLOW_CREDENTIALS = True

# ==================== appointments/models.py ====================
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Doctor(models.Model):
    SPECIALTIES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('oncology', 'Oncology'),
        ('general', 'General Medicine'),
    ]
    
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialty_display()}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.full_name


class TimeSlot(models.Model):
    TIME_CHOICES = [
        ('09:00', '09:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'),
        ('16:00', '04:00 PM'),
        ('17:00', '05:00 PM'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_slots')
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['doctor', 'time']
        ordering = ['time']
    
    def __str__(self):
        return f"{self.doctor.name} - {self.time}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=5)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.patient.full_name} - Dr. {self.doctor.name} - {self.appointment_date}"


# ==================== appointments/serializers.py ====================
from rest_framework import serializers
from .models import Doctor, Patient, Appointment, TimeSlot
from django.contrib.auth.models import User

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_email = serializers.CharField(source='patient.email', read_only=True)
    patient_phone = serializers.CharField(source='patient.phone', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialty = serializers.CharField(source='doctor.get_specialty_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.Serializer):
    patient_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=17)
    doctor_id = serializers.IntegerField()
    appointment_date = serializers.DateField()
    appointment_time = serializers.CharField(max_length=5)
    reason = serializers.CharField()
    
    def create(self, validated_data):
        # Get or create patient
        patient, created = Patient.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'full_name': validated_data['patient_name'],
                'phone': validated_data['phone']
            }
        )
        
        # Get doctor
        doctor = Doctor.objects.get(id=validated_data['doctor_id'])
        
        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            reason=validated_data['reason'],
            status='pending'
        )
        
        return appointment


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# ==================== appointments/views.py ====================
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, TimeSlot
from .serializers import (
    DoctorSerializer, PatientSerializer, AppointmentSerializer,
    AppointmentCreateSerializer, TimeSlotSerializer, UserRegistrationSerializer
)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]  # Change in production
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        doctors = Doctor.objects.filter(is_available=True)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        doctor = self.get_object()
        date = request.query_params.get('date')
        
        if not date:
            return Response(
                {'error': 'Date parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get booked appointments for this doctor on this date
        booked_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            status__in=['pending', 'confirmed']
        ).values_list('appointment_time', flat=True)
        
        # Get all time slots for this doctor
        all_slots = TimeSlot.objects.filter(doctor=doctor, is_available=True)
        
        available_slots = []
        for slot in all_slots:
            if slot.time not in booked_appointments:
                available_slots.append({
                    'time': slot.time,
                    'display': slot.get_time_display()
                })
        
        return Response(available_slots)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]  # Change in production
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient = Patient.objects.get(email=email)
            serializer = self.get_serializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]  # Change in production
    
    def get_queryset(self):
        queryset = Appointment.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        doctor_id = self.request.query_params.get('doctor_id')
        status_param = self.request.query_params.get('status')
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset
    
    def create(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            response_serializer = AppointmentSerializer(appointment)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.notes = request.data.get('notes', '')
        appointment.prescription = request.data.get('prescription', '')
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
def dashboard_stats(request):
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    
    return Response({
        'total_appointments': total_appointments,
        'pending': pending_appointments,
        'confirmed': confirmed_appointments,
        'total_doctors': total_doctors,
        'total_patients': total_patients
    })


# ==================== appointments/urls.py ====================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'appointments', views.AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('dashboard-stats/', views.dashboard_stats, name='dashboard-stats'),
]


# ==================== hospital_appointment/urls.py ====================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('appointments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ==================== appointments/admin.py ====================
from django.contrib import admin
from .models import Doctor, Patient, Appointment, TimeSlot

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'email', 'phone', 'is_available']
    list_filter = ['specialty', 'is_available']
    search_fields = ['name', 'email', 'phone']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'created_at']
    search_fields = ['full_name', 'email', 'phone']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_date', 'doctor']
    search_fields = ['patient__full_name', 'doctor__name']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'time', 'is_available']
    list_filter = ['doctor', 'is_available']


# ==================== SETUP INSTRUCTIONS ====================
"""
1. Create virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Create PostgreSQL database:
   createdb hospital_db

4. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Create superuser:
   python manage.py createsuperuser

6. Run server:
   python manage.py runserver

7. Access admin panel:
   http://localhost:8000/admin

8. API Endpoints:
   - GET  /api/doctors/ - List all doctors
   - POST /api/doctors/ - Create doctor
   - GET  /api/doctors/{id}/ - Get doctor details
   - GET  /api/doctors/available/ - Get available doctors
   - GET  /api/doctors/{id}/available_slots/?date=2025-10-20 - Get available slots
   
   - GET  /api/patients/ - List all patients
   - POST /api/patients/ - Create patient
   - GET  /api/patients/by_email/?email=john@email.com - Get patient by email
   
   - GET  /api/appointments/ - List all appointments
   - POST /api/appointments/ - Book appointment
   - GET  /api/appointments/{id}/ - Get appointment details
   - POST /api/appointments/{id}/confirm/ - Confirm appointment
   - POST /api/appointments/{id}/cancel/ - Cancel appointment
   - POST /api/appointments/{id}/complete/ - Complete appointment
   
   - POST /api/register/ - Register user
   - POST /api/login/ - Login user
   - GET  /api/dashboard-stats/ - Get dashboard statistics

9. Example POST request to book appointment:
   {
     "patient_name": "John Doe",
     "email": "john@email.com",
     "phone": "+1234567890",
     "doctor_id": 1,
     "appointment_date": "2025-10-20",
     "appointment_time": "10:00",
     "reason": "Regular checkup"
   }
"""