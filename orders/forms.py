import re
from django import forms
from orders.models import BOOK_STATUS_CHOICES, Order


class CreateOrderForm(forms.Form): # form is not сonnected with models, we validate the fields ourselves
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()

    def clean_phone_number(self): # custom validator, clean_ - additional validation to the field phone_number
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("The phone number must contain only numbers")

        pattern = r"^\d{10}$"
        if not re.match(pattern, data):
            raise forms.ValidationError("Invalid number format")

        return data
    
class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'order_start', 'order_end']
        
class BookStatusForm(forms.Form):
    order_item_id = forms.IntegerField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=BOOK_STATUS_CHOICES, widget=forms.RadioSelect())
