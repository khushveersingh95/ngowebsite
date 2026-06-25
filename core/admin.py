import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import (
    AnnualReport,
    Banner,
    Campaign,
    Cause,
    ContactQuery,
    Donation,
    FAQ,
    Gallery,
    GalleryCategory,
    PageContent,
    SiteSettings,
    Subscriber,
    TeamMember,
    Testimonial,
    Volunteer,
)


admin.site.site_header = 'Helping Hands Admin'
admin.site.site_title = 'Helping Hands NGO'
admin.site.index_title = 'NGO Management Dashboard'
admin.site.index_template = 'admin/dashboard.html'


@admin.action(description='Export selected volunteers as CSV')
def export_volunteers(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="volunteers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Phone', 'City', 'Skills', 'Availability', 'Message', 'Applied At'])
    for volunteer in queryset:
        writer.writerow([
            volunteer.full_name,
            volunteer.email,
            volunteer.phone,
            volunteer.city,
            volunteer.skills,
            volunteer.availability,
            volunteer.message,
            volunteer.created_at,
        ])
    return response


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Brand', {'fields': ('ngo_name', 'logo', 'favicon', 'mission_statement')}),
        ('Contact', {'fields': ('address', 'email', 'phone')}),
        ('Social Media', {'fields': ('facebook', 'instagram', 'twitter', 'linkedin', 'youtube')}),
    )


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'updated_at')
    search_fields = ('title', 'body')


@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_amount', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'description')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'goal_amount', 'raised_amount', 'progress_percent', 'start_date', 'end_date')
    list_filter = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'media_type', 'is_featured', 'created_at')
    list_filter = ('category', 'media_type', 'is_featured')
    search_fields = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'role', 'story')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'city', 'availability', 'is_reviewed', 'created_at')
    list_filter = ('city', 'is_reviewed', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'city', 'skills')
    actions = [export_volunteers]


@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'phone', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    list_editable = ('is_resolved',)
    search_fields = ('name', 'email', 'phone', 'subject', 'message')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'email', 'amount', 'status', 'razorpay_payment_id', 'paid_at')
    list_filter = ('status', 'paid_at', 'created_at')
    search_fields = ('donor_name', 'email', 'phone', 'razorpay_payment_id', 'razorpay_order_id')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'paid_at')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('email',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role', 'bio')


@admin.register(AnnualReport)
class AnnualReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'is_public', 'created_at')
    list_filter = ('year', 'is_public')
    search_fields = ('title',)
