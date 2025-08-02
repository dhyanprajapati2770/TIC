from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, DoctorProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_verified', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Healthcare Info', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'address', 
                      'profile_picture', 'is_verified')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'blood_group', 'height', 'weight')
    search_fields = ('user__username', 'user__email')


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'years_of_experience', 'is_available', 'rating')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__username', 'license_number', 'specialization')