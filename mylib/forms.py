from django.forms import ModelForm
from django import forms
from .models import Book
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime



class RequestIssueForm(forms.Form):
    return_date=forms.DateField(help_text="max_issue_period = One month ||  fomat:MM/DD/YYYY ")

    def clean_return_date(self):
        data= self.cleaned_data['return_date']

        if data <datetime.date.today():
            raise ValidationError(_('Invalid Date'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date "Not within a month"'))

        return data






