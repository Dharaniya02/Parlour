from django import forms
from .models import Appointment,Profile
from .models import Offer

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'name', 'email', 'phone', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']  # Include 'avatar' for image upload
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'service', 'date', 'time']
        
# class OfferForm(forms.ModelForm):
#     class Meta:
#         model = Offer
#         fields = ['title', 'description', 'discount_percentage']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'discount_percentage', 'active']

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get('discount_percentage')
        if discount_percentage is None:
            raise forms.ValidationError("This field is required.")
        return discount_percentage