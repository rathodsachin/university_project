from django.contrib import admin
from university.models import Institute
from university.models import Branch
from university.models import Fee
from university.models import Students
from .models import PaytmHistory


# Register your models here.
admin.site.register(Institute)
admin.site.register(Branch)
admin.site.register(Fee)
admin.site.register(Students)


class PaytmHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'MID', 'TXNAMOUNT', 'STATUS')


admin.site.register(PaytmHistory, PaytmHistoryAdmin)
