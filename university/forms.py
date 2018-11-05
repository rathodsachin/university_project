from django import forms
from django.contrib.auth.models import User
from .models import Students
from .models import Institute
from .models import Branch
from django.forms.widgets import SelectDateWidget
from django.http import JsonResponse
import datetime


class SignUpForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email_address=forms.EmailField(max_length=40,required=False, help_text='Optional.')
	institute = forms.ModelChoiceField(queryset=Institute.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
#	dob=forms.DateField(widget=SelectDateWidget(years=range(1991,2018)),initial=datetime.date.today)
	class Meta:
		model=Students
		fields=('user_name','password1','first_name','last_name','email_address','phone', 'dob', 'enrollment_number', 'institute','branch', 'course',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['branch'].queryset = Branch.objects.none()