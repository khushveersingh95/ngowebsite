from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .emails import send_basic_email, send_donation_receipt
from .forms import ContactForm, DonationForm, SubscriberForm, VolunteerForm
from .models import (
    AnnualReport,
    Banner,
    Campaign,
    Cause,
    Donation,
    FAQ,
    Gallery,
    GalleryCategory,
    PageContent,
    SiteSettings,
    Subscriber,
    TeamMember,
    Testimonial,
)
from .payments import create_razorpay_order, verify_razorpay_signature


def get_settings():
    return SiteSettings.objects.first()


def home(request):
    context = {
        'banner': Banner.objects.filter(is_active=True).order_by('-updated_at').first(),
        'mission': get_settings(),
        'causes': Cause.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:3],
        'campaigns': Campaign.objects.filter(status='active').order_by('-is_featured', '-created_at')[:3],
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('-created_at')[:6],
        'gallery_items': Gallery.objects.filter(is_featured=True).order_by('-created_at')[:6],
        'faqs': FAQ.objects.filter(is_active=True)[:6],
        'subscriber_form': SubscriberForm(),
        'impact': {
            'donations': Donation.objects.filter(status='paid').count(),
            'volunteers': TeamMember.objects.filter(is_active=True).count() + 125,
            'campaigns': Campaign.objects.filter(status='active').count(),
            'lives': 5000,
        },
    }
    return render(request, 'core/home.html', context)


def about(request):
    content = PageContent.objects.filter(page=PageContent.ABOUT).first()
    return render(request, 'core/about.html', {
        'content': content,
        'team': TeamMember.objects.filter(is_active=True),
        'reports': AnnualReport.objects.filter(is_public=True),
    })


def causes(request):
    return render(request, 'core/causes.html', {'causes': Cause.objects.filter(is_active=True)})


def campaigns(request):
    return render(request, 'core/campaigns.html', {'campaigns': Campaign.objects.exclude(status='draft')})


def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    return render(request, 'core/campaign_detail.html', {'campaign': campaign})


def volunteer(request):
    form = VolunteerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save()
        send_basic_email(
            'Thank you for volunteering',
            f'Dear {application.full_name},\n\nThank you for applying to volunteer with us. Our team will contact you soon.',
            [application.email],
        )
        send_basic_email(
            'New volunteer application',
            f'{application.full_name} from {application.city} applied as a volunteer.\nEmail: {application.email}\nPhone: {application.phone}',
            [settings.ADMIN_EMAIL],
        )
        messages.success(request, 'Your volunteer application was submitted successfully.')
        return redirect('volunteer')
    return render(request, 'core/volunteer.html', {'form': form})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        query = form.save()
        send_basic_email(
            'We received your message',
            f'Dear {query.name},\n\nThank you for contacting us. We will get back to you soon.',
            [query.email],
        )
        send_basic_email(
            f'New contact query: {query.subject}',
            f'{query.name} wrote:\n\n{query.message}\n\nEmail: {query.email}\nPhone: {query.phone}',
            [settings.ADMIN_EMAIL],
        )
        messages.success(request, 'Your message was sent successfully.')
        return redirect('contact')
    return render(request, 'core/contact.html', {'form': form})


def donate(request):
    return render(request, 'core/donate.html', {
        'form': DonationForm(),
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


@require_POST
def create_order(request):
    form = DonationForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    donation = form.save()
    try:
        order = create_razorpay_order(donation.amount, f'donation-{donation.id}')
    except RuntimeError as exc:
        donation.status = 'failed'
        donation.save(update_fields=['status'])
        return JsonResponse({'ok': False, 'message': str(exc)}, status=503)

    donation.razorpay_order_id = order['id']
    donation.save(update_fields=['razorpay_order_id'])
    return JsonResponse({
        'ok': True,
        'order_id': order['id'],
        'amount': order['amount'],
        'currency': order['currency'],
        'key': settings.RAZORPAY_KEY_ID,
        'donation_id': donation.id,
        'name': donation.donor_name,
        'email': donation.email,
        'phone': donation.phone,
    })


@require_POST
def verify_payment(request):
    donation = get_object_or_404(Donation, id=request.POST.get('donation_id'))
    payment_id = request.POST.get('razorpay_payment_id', '')
    order_id = request.POST.get('razorpay_order_id', '')
    signature = request.POST.get('razorpay_signature', '')
    if order_id != donation.razorpay_order_id or not verify_razorpay_signature(order_id, payment_id, signature):
        donation.status = 'failed'
        donation.save(update_fields=['status'])
        messages.error(request, 'Payment verification failed. Please contact support if money was debited.')
        return redirect('donate')

    donation.razorpay_payment_id = payment_id
    donation.razorpay_signature = signature
    donation.status = 'paid'
    donation.paid_at = timezone.now()
    donation.save()
    send_donation_receipt(donation, get_settings())
    return redirect(reverse('success', args=[donation.id]))


def success(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, status='paid')
    return render(request, 'core/success.html', {'donation': donation})


def gallery(request):
    category_slug = request.GET.get('category')
    items = Gallery.objects.select_related('category').order_by('-created_at')
    if category_slug:
        items = items.filter(category__slug=category_slug)
    return render(request, 'core/gallery.html', {
        'gallery_items': items,
        'categories': GalleryCategory.objects.all(),
        'active_category': category_slug,
    })


def faq(request):
    return render(request, 'core/faq.html', {'faqs': FAQ.objects.filter(is_active=True)})


@require_POST
def newsletter(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        Subscriber.objects.get_or_create(email=form.cleaned_data['email'])
        messages.success(request, 'You have been subscribed to our newsletter.')
    else:
        messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def static_page(request, page):
    content = get_object_or_404(PageContent, page=page)
    return render(request, 'core/static_page.html', {'content': content})
