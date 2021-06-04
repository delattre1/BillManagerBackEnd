from django.contrib import admin
from .models import Bill, BlackListWords

admin.site.register(Bill)
admin.site.register(BlackListWords)
# Register your models here.
