from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import UserActivity, Analytics, SystemHealth, Notification, UserReport
from symptoms.models import SymptomCheck
from diseases.models import DiseasePrediction
from pharmacy.models import Order
from users.models import User


@login_required
def dashboard(request):
    """User dashboard view."""
    # Get user's recent activities
    recent_activities = UserActivity.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Get user's recent symptom checks
    recent_symptom_checks = SymptomCheck.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get user's recent disease predictions
    recent_predictions = DiseasePrediction.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
    
    return render(request, 'dashboard/dashboard.html', {
        'recent_activities': recent_activities,
        'recent_symptom_checks': recent_symptom_checks,
        'recent_predictions': recent_predictions,
        'recent_orders': recent_orders,
        'unread_notifications': unread_notifications,
    })


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard view."""
    # Get overall statistics
    total_users = User.objects.count()
    total_symptom_checks = SymptomCheck.objects.count()
    total_predictions = DiseasePrediction.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Get recent activities
    recent_activities = UserActivity.objects.all().order_by('-created_at')[:20]
    
    # Get system health
    system_health = SystemHealth.objects.all()
    
    # Get recent reports
    recent_reports = UserReport.objects.all().order_by('-created_at')[:10]
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'total_users': total_users,
        'total_symptom_checks': total_symptom_checks,
        'total_predictions': total_predictions,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_activities': recent_activities,
        'system_health': system_health,
        'recent_reports': recent_reports,
    })


@staff_member_required
def analytics(request):
    """Analytics view."""
    # Get date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get analytics data
    analytics_data = Analytics.objects.filter(date__range=[start_date, end_date]).order_by('date')
    
    return render(request, 'dashboard/analytics.html', {
        'analytics_data': analytics_data,
        'start_date': start_date,
        'end_date': end_date,
    })


@staff_member_required
def reports(request):
    """Reports view."""
    reports = UserReport.objects.all().order_by('-created_at')
    
    return render(request, 'dashboard/reports.html', {
        'reports': reports
    })


@login_required
def settings(request):
    """Settings view."""
    return render(request, 'dashboard/settings.html')


# API Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_analytics(request):
    """API endpoint for analytics data."""
    # Get user's analytics
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    activity_data = []
    for activity in user_activities:
        activity_data.append({
            'id': activity.id,
            'activity_type': activity.activity_type,
            'description': activity.description,
            'created_at': activity.created_at.isoformat(),
        })
    
    return Response({
        'activities': activity_data,
        'total_activities': user_activities.count(),
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_admin_analytics(request):
    """API endpoint for admin analytics."""
    # Get overall statistics
    total_users = User.objects.count()
    total_symptom_checks = SymptomCheck.objects.count()
    total_predictions = DiseasePrediction.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Get daily statistics for the last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    daily_stats = []
    current_date = start_date
    while current_date <= end_date:
        daily_users = User.objects.filter(date_joined__date=current_date).count()
        daily_checks = SymptomCheck.objects.filter(created_at__date=current_date).count()
        daily_predictions = DiseasePrediction.objects.filter(created_at__date=current_date).count()
        daily_orders = Order.objects.filter(created_at__date=current_date).count()
        daily_revenue = Order.objects.filter(created_at__date=current_date, payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
        
        daily_stats.append({
            'date': current_date.isoformat(),
            'users': daily_users,
            'symptom_checks': daily_checks,
            'predictions': daily_predictions,
            'orders': daily_orders,
            'revenue': float(daily_revenue),
        })
        
        current_date += timedelta(days=1)
    
    return Response({
        'total_users': total_users,
        'total_symptom_checks': total_symptom_checks,
        'total_predictions': total_predictions,
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'daily_stats': daily_stats,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_reports(request):
    """API endpoint for reports."""
    reports = UserReport.objects.all().order_by('-created_at')
    
    report_data = []
    for report in reports:
        report_data.append({
            'id': report.id,
            'user': report.user.username,
            'report_type': report.report_type,
            'title': report.title,
            'description': report.description,
            'priority': report.priority,
            'status': report.status,
            'created_at': report.created_at.isoformat(),
        })
    
    return Response({
        'reports': report_data,
        'total_reports': reports.count(),
    })
