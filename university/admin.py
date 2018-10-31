from django.contrib import admin
from university.models import Institute
from university.models import Branch
from university.models import Fee
from university.models import Students
# Register your models here.
admin.site.register(Institute)
admin.site.register(Branch)
admin.site.register(Fee)
admin.site.register(Students)