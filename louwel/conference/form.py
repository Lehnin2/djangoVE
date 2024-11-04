from django import forms
from .models import Conference
class conferenceform(forms.ModelForm):
    class Meta:
        model=Conference
        fields="__all__"
    start_date=forms.DateField(
    label="conference start date",
        widget=forms.DateInput(
            attrs={
                'type':'date'
            }
        )
        )
    end_date=forms.DateField(
        label="conference start date",
        widget=forms.DateInput(
            attrs={
                'type':'date'
            }
        )
        )
        