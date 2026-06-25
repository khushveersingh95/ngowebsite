from django import forms

from .models import ContactQuery, Donation, Subscriber, Volunteer


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            field.widget.attrs['class'] = field.widget.attrs.get('class', css_class)


class VolunteerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['full_name', 'email', 'phone', 'city', 'skills', 'availability', 'message']
        widgets = {'message': forms.Textarea(attrs={'rows': 4})}


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ContactQuery
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class DonationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'email', 'phone', 'amount']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Donation amount must be greater than zero.')
        return amount


class SubscriberForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
