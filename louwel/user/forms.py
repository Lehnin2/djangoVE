from django import forms
from .models import Participant
class participantform(forms.ModelForm):
    class Meta:
        model=Participant
        fields=['username','email','first_name','last_name','cin','participant_category']
    def save(self,commit=True):
        user=super().save(commit=False)
        print()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
   
        