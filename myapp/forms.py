# app - forms.py file new

from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields =('name','photo','email','password','mobile_number','date_of_birth')
        widgets = {
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'password': forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Enter a password',
            }),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'e.g. Alex Morgan',
            'email': 'name@example.com',
            'mobile_number': 'e.g. +1 555 010 2040',
        }
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

        self.fields['photo'].required = False
        self.fields['photo'].help_text = 'Optional. Add a profile photo if you have one.'

        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Leave blank to keep the current password.'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password and self.instance.pk:
            return self.instance.password
        return password
