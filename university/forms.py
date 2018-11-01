from django import forms
from django.contrib.auth.models import User
from .models import Students
from .models import Institute
from django.forms.widgets import SelectDateWidget
import datetime


class SignUpForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')	
	institute = forms.ModelChoiceField(queryset=Institute.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	dob=forms.DateField(widget=SelectDateWidget(years=range(2018, 1991)),initial=datetime.date.today)
	class Meta:
		model=Students
		fields=('user_name','password1','first_name','last_name','phone', 'dob', 'enrollment_number', 'institute','branch', 'course',)
