from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'donors', views.DonorViewSet)
router.register(r'inventory', views.BloodInventoryViewSet)
router.register(r'requests', views.BloodRequestViewSet)
router.register(r'donations', views.DonationRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('dashboard/', views.dashboard_stats),
]