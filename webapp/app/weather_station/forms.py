from django import forms
import datetime


class DateHistoryForm(forms.Form):
    date_from = forms.DateField(initial=datetime.date.today, label="Data Início")
    date_to = forms.DateField(initial=datetime.date.today, label="Data Fim")
