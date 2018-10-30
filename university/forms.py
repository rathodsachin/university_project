from django import forms
from django.contrib.auth.models import User
from .models import Students
from .models import Institute

class SignUpForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	Institute = forms.ModelChoiceField(queryset=Institute.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

	class Meta:
		model=Students
		fields=('userName', 'enrollment_number', 'branch', 'course', 'phone', 'dob', )
