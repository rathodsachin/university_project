from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import uuid
from django.conf import settings
from django.utils import timezone

class Institute(TimeStampedModel):

	name = models.CharField(max_length=40,help_text='Enter Institute Name.',unique=True)
	slug = models.SlugField(max_length=100)
	logo = models.ImageField(upload_to = 'media',null=True, blank=True)
	email_address = models.EmailField(max_length=40,unique=True,help_text='Enter Email.')
	phone = PhoneNumberField()
	brochure = models.FileField(upload_to='media/')
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Branch(TimeStampedModel):
	   
	name = models.CharField(max_length=40,help_text='Enter Branch Name.',unique=True)
	slug = models.SlugField(max_length=100)	
	email_address = models.EmailField(max_length=40,unique=True,help_text='Enter Email.')
	address=models.TextField(max_length=500, blank=True)
	phone = PhoneNumberField()
	brochure = models.FileField(upload_to='media/')
	is_active = models.BooleanField(default=True)
	institute = models.ForeignKey(Institute, on_delete=models.CASCADE)

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
	userName = models.OneToOneField(User, on_delete=models.CASCADE,related_name="students")
	user_name=models.CharField(unique=True,max_length=15)
	password1=models.CharField(max_length=15)
	enrollment_number=models.CharField(unique=True,max_length=15)
	institute= models.ForeignKey(Institute, on_delete=models.CASCADE,null=True,blank=True)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True,blank=True)
	course = models.CharField(max_length=9,choices=COURSE_CHOICE,default="M.TECH")
	phone = PhoneNumberField()
	dob = models.DateField(default=datetime.date.today)
	is_active = models.BooleanField(default=True)	

	# USERNAME_FIELD = 'user_name'

	def __str__(self):
		return self.userName.username



#Institute = forms.ModelChoiceField(queryset=InstituteModel.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

class Transaction(TimeStampedModel):

	FEE_STATUS=(
		("Pending","Pending"),
		("Completed","Completed"),
		("Failed","Failed"),
		)

	uuid = models.UUIDField(primary_key=True)
	students=models.ForeignKey(Students, on_delete=models.CASCADE)
	paid_amount=models.IntegerField()
	status=models.CharField(max_length=10,choices=FEE_STATUS,default="Pending")


	# data = {
	# 'uuid': uuid,
	# 'user': students,
	# 'paid_amount': paid_amount,
	# 'status': status,
	# }
	# request_dump = JSONField(data) 



class PaytmHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,related_name='rel_payment_paytm')
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.IntegerField('TXN ID')
    BANKTXNID = models.IntegerField('BANK TXN ID', null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    class Meta:
        app_label = 'paytm'

    def __unicode__(self):
        return self.STATUS


