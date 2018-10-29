from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Institute(TimeStampedModel):

	name = models.CharField(max_length=40,help_text='Enter Institute Name.',unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	logo = models.ImageField(upload_to = 'media/',null=True, blank=True)
	email_address = models.EmailField(max_length=40,unique=True,help_text='Enter Email.')
	phone = PhoneNumberField()
	brochure = models.FileField(upload_to='media/')
	is_active = models.BooleanField(default=True)

	def save(self):
		if not self.id:
			self.slug = slugify(self.name)

		super(Test, self).save()


class Branch(TimeStampedModel):

	institute = models.ForeignKey(Institute, on_delete=models.CASCADE)    
	name = models.CharField(max_length=40,help_text='Enter Branch Name.')
	slug = models.SlugField(max_length=100, unique=True)	
	email_address = models.EmailField(max_length=40,unique=True,help_text='Enter Email.')
	address=models.TextField(max_length=500, blank=True)
	phone = PhoneNumberField()
	brochure = models.FileField(upload_to='media/')
	is_active = models.BooleanField(default=True)


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


class Students(TimeStampedModel):
	
	- Enrollment number(unique)
        - Branch(Relation)
        - Course(MBA, B.Tech , etc)
        - Include personal detials(Contact,DOB etc)
        - is_active

    user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = PhoneNumberField()
	dob = models.DateField(default=datetime.date.today)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)

