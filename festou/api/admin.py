from django.contrib import admin
from .models import User, Place, Transaction
# Register your models here.
admin.site.register(Place)
admin.site.register(User)
admin.site.register(Transaction)