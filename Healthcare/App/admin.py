from django.contrib import admin
from .models import Doctor, Patient, User, Appointment
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Appointment)
