import hmac
import hashlib

from django.conf import settings


def create_razorpay_order(amount_rupees, receipt):
    amount_paise = int(float(amount_rupees) * 100)
    try:
        import razorpay
    except Exception as exc:
        raise RuntimeError('Install razorpay and configure keys before accepting live payments.') from exc

    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        raise RuntimeError('Razorpay keys are missing.')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    return client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': receipt,
        'payment_capture': 1,
    })


def verify_razorpay_signature(order_id, payment_id, signature):
    payload = f'{order_id}|{payment_id}'.encode()
    secret = settings.RAZORPAY_KEY_SECRET.encode()
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
