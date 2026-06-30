from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Donor, BloodInventory, BloodRequest, DonationRecord
from .serializers import (
    DonorSerializer, BloodInventorySerializer,
    BloodRequestSerializer, DonationRecordSerializer,
    UserSerializer
)


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = DonorSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=None)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class BloodInventoryViewSet(viewsets.ModelViewSet):
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer


class BloodRequestViewSet(viewsets.ModelViewSet):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer


class DonationRecordViewSet(viewsets.ModelViewSet):
    queryset = DonationRecord.objects.all()
    serializer_class = DonationRecordSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'donor')

    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email or '',
        password=password
    )
    user.first_name = role
    user.save()

    return Response(
        {'message': 'Account created successfully'},
        status=status.HTTP_201_CREATED
    )


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'username': user.username,
            'email': user.email,
            'role': user.first_name,
        })
    return Response(
        {'error': 'Invalid username or password'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_stats(request):
    try:
        stats = {
            'total_donors': Donor.objects.count(),
            'total_requests': BloodRequest.objects.count(),
            'pending_requests': BloodRequest.objects.filter(
                status='pending'
            ).count(),
            'critical_requests': BloodRequest.objects.filter(
                priority='critical'
            ).count(),
            'inventory': BloodInventorySerializer(
                BloodInventory.objects.all(), many=True
            ).data
        }
        return Response(stats)
    except Exception as e:
        return Response({'error': str(e)})