from django.forms import ModelForm
from django import forms
from .models import Book
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RequestIssueForm(forms.Form):
    return_date=forms.DateField(help_text="max_issue_period = One month ||  fomat:MM/DD/YYYY ")

    def clean_return_date(self):
        data= self.cleaned_data['return_date']

        if data <datetime.date.today():
            raise ValidationError(_('Invalid Date'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date "Not within a month"'))

        return data


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain
            alphanumeric
            characters and the
            underscore.
            ')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')





