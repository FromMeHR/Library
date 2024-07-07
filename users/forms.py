import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User, Abonement

class UserLoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
    # username = forms.CharField()
    # password = forms.CharField()
    
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={"autofocus": True, 
    #                                   "class":"form-control",
    #                                   "placeholder":"Введите ваше имя пользователя"
    #                                   })
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                       "class":"form-control",
    #                                       "placeholder":"Введите ваш пароль"                                         
    #                                       }),
    # )
class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    
class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "image",
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "email",
        )
    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    phone_number = forms.CharField() 
    email = forms.CharField()
    
    def clean_phone_number(self): # custom validator, clean_ - additional validation to the field phone_number
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("The phone number must contain only numbers")

        pattern = r"^\d{10}$"
        if not re.match(pattern, data):
            raise forms.ValidationError("Invalid number format")

        return data
    
class AbonementForm(forms.Form):
    radius = forms.ChoiceField(choices=[
        ('1_month', '1 місяць - 100 грн'),
        ('1_year', '1 рік - 500 грн'),
    ], widget=forms.RadioSelect)
    
    