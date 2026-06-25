from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('causes/', views.causes, name='causes'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('campaigns/<slug:slug>/', views.campaign_detail, name='campaign_detail'),
    path('donate/', views.donate, name='donate'),
    path('donate/create-order/', views.create_order, name='create_order'),
    path('donate/verify/', views.verify_payment, name='verify_payment'),
    path('success/<int:donation_id>/', views.success, name='success'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('privacy-policy/', views.static_page, {'page': 'privacy'}, name='privacy'),
    path('terms-and-conditions/', views.static_page, {'page': 'terms'}, name='terms'),
]
