from django.contrib import admin
from .models import Donor, BloodInventory, BloodRequest, DonationRecord

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'blood_type', 'location', 'status']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['blood_type', 'status']

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ['blood_type', 'units_available', 'minimum_threshold', 'last_updated']

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'blood_type', 'units_needed', 'priority', 'status']
    list_filter = ['priority', 'status']

@admin.register(DonationRecord)
class DonationRecordAdmin(admin.ModelAdmin):
    list_display = ['blood_type', 'units', 'transaction_type', 'date']
