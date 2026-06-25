from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string


def send_basic_email(subject, message, recipients):
    if not recipients:
        return
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)


def build_receipt_pdf(donation, site_settings):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except Exception:
        return None

    buffer = BytesIO()
    receipt = canvas.Canvas(buffer, pagesize=A4)
    receipt.setTitle('Donation Receipt')
    receipt.setFont('Helvetica-Bold', 18)
    receipt.drawString(72, 780, 'Donation Receipt')
    receipt.setFont('Helvetica', 11)
    receipt.drawString(72, 750, f'NGO: {getattr(site_settings, "ngo_name", "Helping Hands NGO")}')
    receipt.drawString(72, 725, f'Donor: {donation.donor_name}')
    receipt.drawString(72, 700, f'Amount: INR {donation.amount}')
    receipt.drawString(72, 675, f'Payment ID: {donation.razorpay_payment_id}')
    receipt.drawString(72, 650, f'Date: {donation.paid_at:%d %B %Y, %I:%M %p}')
    receipt.drawString(72, 610, 'Thank you for supporting our work.')
    receipt.showPage()
    receipt.save()
    buffer.seek(0)
    return buffer.getvalue()


def send_donation_receipt(donation, site_settings):
    body = render_to_string('core/email_donation.txt', {'donation': donation, 'site_settings': site_settings})
    email = EmailMessage(
        'Thank you for your donation',
        body,
        settings.DEFAULT_FROM_EMAIL,
        [donation.email],
    )
    receipt_pdf = build_receipt_pdf(donation, site_settings)
    if receipt_pdf:
        email.attach(f'donation-receipt-{donation.razorpay_payment_id}.pdf', receipt_pdf, 'application/pdf')
    email.send(fail_silently=True)
