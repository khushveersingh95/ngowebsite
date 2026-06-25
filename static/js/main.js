function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

document.addEventListener('DOMContentLoaded', () => {
  const donationForm = document.getElementById('donation-form');
  if (donationForm && window.donationConfig) {
    donationForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const submitButton = donationForm.querySelector('button[type="submit"]');
      submitButton.disabled = true;
      submitButton.textContent = 'Creating order...';

      try {
        const response = await fetch(window.donationConfig.createOrderUrl, {
          method: 'POST',
          headers: {'X-CSRFToken': getCookie('csrftoken')},
          body: new FormData(donationForm),
        });
        const data = await response.json();
        if (!data.ok) {
          alert(data.message || 'Please check donation details.');
          return;
        }

        const checkout = new Razorpay({
          key: data.key,
          amount: data.amount,
          currency: data.currency,
          name: window.donationConfig.ngoName,
          description: 'Donation',
          order_id: data.order_id,
          prefill: {name: data.name, email: data.email, contact: data.phone},
          theme: {color: '#1f7a4d'},
          handler(payment) {
            document.getElementById('verify-donation-id').value = data.donation_id;
            document.getElementById('verify-payment-id').value = payment.razorpay_payment_id;
            document.getElementById('verify-order-id').value = payment.razorpay_order_id;
            document.getElementById('verify-signature').value = payment.razorpay_signature;
            document.getElementById('payment-verify-form').submit();
          },
        });
        checkout.open();
      } catch (error) {
        alert('Unable to start payment. Please try again.');
      } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Proceed to Pay';
      }
    });
  }

  const modal = document.getElementById('lightboxModal');
  if (modal) {
    const preview = modal.querySelector('img');
    document.querySelectorAll('.lightbox').forEach((link) => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        preview.src = link.href;
        modal.classList.add('is-open');
      });
    });
    modal.querySelector('.btn-close').addEventListener('click', () => modal.classList.remove('is-open'));
    modal.addEventListener('click', (event) => {
      if (event.target === modal) modal.classList.remove('is-open');
    });
  }
});
