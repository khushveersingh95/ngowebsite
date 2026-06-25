from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):
    ngo_name = models.CharField(max_length=160, default='Helping Hands NGO')
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    mission_statement = models.TextField(default='Serving communities with compassion, dignity, and long-term support.')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.ngo_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            self.pk = SiteSettings.objects.first().pk
        return super().save(*args, **kwargs)


class Banner(TimeStampedModel):
    title = models.CharField(max_length=220)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/', blank=True)
    button_text = models.CharField(max_length=60, default='Donate Now')
    button_link = models.CharField(max_length=160, default='/donate/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PageContent(TimeStampedModel):
    ABOUT = 'about'
    PRIVACY = 'privacy'
    TERMS = 'terms'
    PAGE_CHOICES = [
        (ABOUT, 'About Us'),
        (PRIVACY, 'Privacy Policy'),
        (TERMS, 'Terms & Conditions'),
    ]
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=180)
    body = models.TextField()
    image = models.ImageField(upload_to='pages/', blank=True)

    def __str__(self):
        return self.get_page_display()


class Cause(TimeStampedModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='causes/', blank=True)
    short_description = models.CharField(max_length=260)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Campaign(TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    banner_image = models.ImageField(upload_to='campaigns/', blank=True)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def progress_percent(self):
        if not self.goal_amount:
            return 0
        return min(round((float(self.raised_amount) / float(self.goal_amount)) * 100), 100)

    def get_absolute_url(self):
        return reverse('campaign_detail', args=[self.slug])


class GalleryCategory(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Gallery categories'

    def __str__(self):
        return self.name


class Gallery(TimeStampedModel):
    IMAGE = 'image'
    VIDEO = 'video'
    MEDIA_CHOICES = [(IMAGE, 'Image'), (VIDEO, 'Video')]
    title = models.CharField(max_length=160)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES, default=IMAGE)
    image = models.ImageField(upload_to='gallery/', blank=True)
    video_url = models.URLField(blank=True, help_text='Paste a YouTube/Vimeo URL for videos.')
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    story = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=220)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class Volunteer(TimeStampedModel):
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    skills = models.CharField(max_length=240)
    availability = models.CharField(max_length=160)
    message = models.TextField(blank=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class ContactQuery(TimeStampedModel):
    name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Contact queries'

    def __str__(self):
        return f'{self.subject} - {self.name}'


class Donation(TimeStampedModel):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    donor_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=120, blank=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=120, blank=True)
    razorpay_signature = models.CharField(max_length=240, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.donor_name} - {self.amount}'


class Subscriber(TimeStampedModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='team/', blank=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class AnnualReport(TimeStampedModel):
    title = models.CharField(max_length=180)
    year = models.PositiveIntegerField()
    report_file = models.FileField(upload_to='annual-reports/')
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f'{self.title} ({self.year})'
