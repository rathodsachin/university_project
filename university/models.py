from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import uuid
import json


# Create your models here.

class Institute(TimeStampedModel):

	name = models.CharField(max_length=40,help_text='Enter Institute Name.',unique=True)
	slug = models.SlugField(max_length=100)
	logo = models.ImageField(upload_to = 'media',null=True, blank=True)
	email_address = models.EmailField(max_length=40,unique=True,help_text='Enter Email.')
	phone = PhoneNumberField()
	brochure = models.FileField(upload_to='media/')
	is_active = models.BooleanField(default=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(Institute, self).save()

	def __str__(self):
		return self.name


class Branch(TimeStampedModel):

	institute = models.ForeignKey(Institute, on_delete=models.CASCADE)    
	name = models.CharField(max_length=40,help_text='Enter Branch Name.',unique=True)
	slug = models.SlugField(max_length=100)	
	email_address = models.EmailField(max_length=40,unique=True,help_text='Enter Email.')
	address=models.TextField(max_length=500, blank=True)
	phone = PhoneNumberField()
	brochure = models.FileField(upload_to='media/')
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Fee(TimeStampedModel):

	FEE_CHOICES = (
	    ("admission", "Admission"),
	    ("exam", "Exam"),
	    ("library", "Library"),	    
	    ("sport", "Sport"),
	)

	fee_type=models.CharField(max_length=9,
                  choices=FEE_CHOICES,
                  default="admission")

	amount=models.IntegerField()
	is_active = models.BooleanField(default=True)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

	def __str__(self):
		return self.fee_type


class Students(TimeStampedModel):

	COURSE_CHOICE=(
		("M.TECH","M.TECH"),
		("B.TECH","B.TECH"),
		("MCA","MCA"),
		("BCA","BCA"),		
		)        
	userName = models.OneToOneField(User, on_delete=models.CASCADE)
	enrollment_number=models.CharField(unique=True,max_length=15)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
	course = models.CharField(max_length=9,choices=COURSE_CHOICE,default="M.TECH")
	phone = PhoneNumberField()
	dob = models.DateField(default=datetime.date.today)
	is_active = models.BooleanField(default=True)	

	def __str__(self):
		return self.userName.username

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Students.objects.create(userName=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

#Institute = forms.ModelChoiceField(queryset=InstituteModel.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

class Transaction(TimeStampedModel):

	FEE_STATUS=(
		("Pending","Pending"),
		("Completed","Completed"),
		("Failed","Failed"),
		)

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	students=models.ForeignKey(Students, on_delete=models.CASCADE)
	paid_amount=models.IntegerField()
	status=models.CharField(max_length=10,choices=FEE_STATUS,default="Pending")


	data = {
	'uuid': uuid,
	'user': students,
	'paid_amount': paid_amount,
	'status': status,
	}
	request_dump =json.dumps(data)
