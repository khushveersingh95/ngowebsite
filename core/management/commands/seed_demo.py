from decimal import Decimal

from django.core.management.base import BaseCommand

from core.models import Banner, Campaign, Cause, FAQ, PageContent, SiteSettings, Testimonial


class Command(BaseCommand):
    help = 'Create starter CMS content for local development.'

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'ngo_name': 'Helping Hands NGO',
                'address': '123 Community Road, New Delhi, India',
                'email': 'info@helpinghands.org',
                'phone': '+91 98765 43210',
                'mission_statement': 'We mobilize resources, volunteers, and local partnerships to support education, health, and emergency relief.',
            },
        )
        Banner.objects.get_or_create(
            title='Together for a kinder tomorrow',
            defaults={
                'subtitle': 'Support campaigns, volunteer your skills, and help communities thrive.',
                'button_text': 'Donate Now',
                'button_link': '/donate/',
                'is_active': True,
            },
        )
        PageContent.objects.get_or_create(
            page=PageContent.ABOUT,
            defaults={'title': 'About Helping Hands', 'body': 'Helping Hands NGO works with communities to deliver relief, education support, healthcare access, and dignity-first social programs.'},
        )
        PageContent.objects.get_or_create(
            page=PageContent.PRIVACY,
            defaults={'title': 'Privacy Policy', 'body': 'We collect only the information needed to respond to queries, process donations, and manage volunteer applications. We do not sell personal data.'},
        )
        PageContent.objects.get_or_create(
            page=PageContent.TERMS,
            defaults={'title': 'Terms & Conditions', 'body': 'By using this website, you agree to provide accurate information and use the donation and contact systems responsibly.'},
        )
        for title, slug, summary in [
            ('Education for Every Child', 'education-for-every-child', 'Learning kits, tuition support, and school readiness programs.'),
            ('Community Health Camps', 'community-health-camps', 'Preventive care and health awareness in underserved areas.'),
            ('Emergency Relief', 'emergency-relief', 'Rapid support during floods, fires, and local emergencies.'),
        ]:
            Cause.objects.get_or_create(
                slug=slug,
                defaults={'title': title, 'short_description': summary, 'description': summary, 'goal_amount': Decimal('100000.00'), 'is_featured': True},
            )
        Campaign.objects.get_or_create(
            slug='winter-relief-drive',
            defaults={'title': 'Winter Relief Drive', 'description': 'Help distribute blankets, meals, and health kits to families during winter.', 'goal_amount': Decimal('250000.00'), 'raised_amount': Decimal('87500.00'), 'is_featured': True},
        )
        Testimonial.objects.get_or_create(
            name='Anita Sharma',
            defaults={'role': 'Program beneficiary', 'story': 'Helping Hands supported my children with school supplies and mentoring when we needed it most.', 'rating': 5},
        )
        FAQ.objects.get_or_create(question='How can I donate?', defaults={'answer': 'Use the Donate page to make a secure Razorpay payment.', 'order': 1})
        FAQ.objects.get_or_create(question='Can I volunteer part-time?', defaults={'answer': 'Yes. Share your availability through the volunteer form and our team will contact you.', 'order': 2})
        self.stdout.write(self.style.SUCCESS('Demo CMS content created.'))
