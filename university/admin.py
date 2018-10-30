from django.contrib import admin
from university.models import Institute
from university.models import Branch
from university.models import Fee
# Register your models here.
admin.site.register(Institute)
admin.site.register(Branch)
admin.site.register(Fee)