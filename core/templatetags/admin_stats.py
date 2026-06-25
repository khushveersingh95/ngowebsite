from django import template
from django.db.models import Sum

from core.models import Campaign, ContactQuery, Donation, Volunteer

register = template.Library()


@register.simple_tag
def dashboard_stats():
    paid_donations = Donation.objects.filter(status='paid')
    return {
        'total_donations': paid_donations.aggregate(total=Sum('amount'))['total'] or 0,
        'total_volunteers': Volunteer.objects.count(),
        'total_queries': ContactQuery.objects.count(),
        'active_campaigns': Campaign.objects.filter(status='active').count(),
        'recent_donations': Donation.objects.order_by('-created_at')[:5],
        'recent_volunteers': Volunteer.objects.order_by('-created_at')[:5],
    }
