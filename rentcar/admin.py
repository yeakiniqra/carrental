from django.contrib import admin
from .models import Owner, UploadCar, Booking, ContactMessage

# Register your models here.
admin.site.register(Owner)
admin.site.register(UploadCar)
admin.site.register(Booking)
admin.site.register(ContactMessage)