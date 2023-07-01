from django.contrib import admin
from home.models import *
admin.register(Store,User,Product,Cart)(admin.ModelAdmin)
# Register your models here.
