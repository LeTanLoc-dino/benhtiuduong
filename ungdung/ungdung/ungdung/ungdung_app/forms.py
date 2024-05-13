from django import forms
from .models import HealthInfo

class HealthInfoForm(forms.ModelForm):
    class Meta:
        model = HealthInfo
        fields = ['patient', 'checkup_date', 'blood_pressure', 'heart_disease', 'smoking', 'bmi', 'hba1c', 'blood_glucose']
