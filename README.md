# Helping Hands NGO Management System

A production-ready Django NGO website with dynamic CMS content, volunteer/contact management, newsletter subscriptions, campaign tracking, gallery management, custom admin dashboard, SMTP email, and Razorpay donations.

## Features

- Admin-managed homepage banner, hero text, about content, causes, campaigns, gallery, testimonials, FAQ, reports, team, contact details, and social links.
- Volunteer applications stored in the database, searchable in admin, exportable as CSV, with volunteer and admin email notifications.
- Contact queries stored in the database, searchable in admin, with resolved/unresolved status and email notifications.
- Razorpay donation flow with order creation, HMAC signature verification, donation persistence, success page, receipt email, and optional PDF receipt attachment.
- Dynamic campaign progress bars based on raised and goal amounts.
- Masonry gallery with category filtering, video links, and image lightbox.
- SQLite for development and PostgreSQL-ready production settings.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for admin.

## Razorpay Setup

1. Create a Razorpay account and open the Dashboard.
2. Go to **Account & Settings > API Keys**.
3. Generate a test or live key pair.
4. Add `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` to `.env`.
5. Restart Django.

The server creates Razorpay orders from `/donate/create-order/` and verifies the returned `razorpay_order_id`, `razorpay_payment_id`, and `razorpay_signature` at `/donate/verify/`.

## Gmail SMTP Setup

1. Enable 2-Step Verification on the Gmail account.
2. Create an App Password from Google Account security settings.
3. Put the email in `EMAIL_HOST_USER`.
4. Put the app password in `EMAIL_HOST_PASSWORD`.
5. Set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`.

For local development without sending emails, use:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## PostgreSQL Setup

Set these variables in `.env`:

```env
DATABASE_URL=postgres
POSTGRES_DB=helping_hands
POSTGRES_USER=helping_hands_user
POSTGRES_PASSWORD=strong-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Run:

```bash
python manage.py migrate
```

## Admin Dashboard

The Django admin dashboard shows:

- Total paid donations
- Volunteer count
- Contact query count
- Active campaigns
- Recent donations
- Recent volunteers

Volunteers can be exported using the admin action **Export selected volunteers as CSV**.

## Deployment Notes

### Hostinger VPS

1. Install Python, PostgreSQL, Nginx, and system build tools.
2. Clone/upload the project to the server.
3. Create a virtual environment and install `requirements.txt`.
4. Configure `.env` with `DEBUG=False`, your domain in `ALLOWED_HOSTS`, PostgreSQL, SMTP, and Razorpay keys.
5. Run `python manage.py migrate` and `python manage.py collectstatic`.
6. Run Gunicorn:

```bash
gunicorn ngo_project.wsgi:application --bind 127.0.0.1:8001
```

7. Configure Nginx to proxy to Gunicorn and serve `/static/` and `/media/`.
8. Enable HTTPS with Certbot.

### Render

1. Create a new Web Service from the repository.
2. Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

3. Start command:

```bash
gunicorn ngo_project.wsgi:application
```

4. Add environment variables from `.env.example`.
5. Add a PostgreSQL database and map its values to the Postgres env vars.

### PythonAnywhere

1. Upload the project or clone it in the Files console.
2. Create a virtualenv and install `requirements.txt`.
3. Configure environment variables in the WSGI file or a `.env` file.
4. Set the WSGI application to `ngo_project.wsgi:application`.
5. Configure static files:
   - URL: `/static/`, directory: `staticfiles`
   - URL: `/media/`, directory: `media`
6. Run migrations from a Bash console.

## Production Checklist

- Set `DEBUG=False`.
- Set a strong `SECRET_KEY`.
- Add the real domain to `ALLOWED_HOSTS`.
- Use PostgreSQL.
- Configure SMTP and Razorpay live keys.
- Run `collectstatic`.
- Set `CSRF_COOKIE_SECURE=True`, `SESSION_COOKIE_SECURE=True`, and `SECURE_SSL_REDIRECT=True` behind HTTPS.
- Back up the database and media files regularly.
