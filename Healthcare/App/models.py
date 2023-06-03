from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    age = models.CharField(max_length=20)

    def __str__(self):
        return "%s" % self.user


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    Qualification = models.CharField(max_length=100, null=True)
    specialization = models.CharField(max_length=200)

    def __str__(self):
        return "%s %s %s  " % (self.user, self.Qualification, self.specialization)


class Appointment(models.Model):
    class Meta:
        unique_together = ('doctor', 'date', 'timeslot')

    TIMESLOT_LIST = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
        (8, '17:00 – 17:30'),
        (9, '18:00 – 18:30'),
    )
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, null=False)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=True)
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot: IntegerField = models.IntegerField(choices=TIMESLOT_LIST, null=False)
    disease = models.CharField(max_length=100, null=False)
    BP = models.CharField(max_length=30, help_text="Blood pressure=120/80", null=True)
    BMI = models.IntegerField(help_text="Body to mass index = 25",  null=True)
    BS = models.CharField(max_length=30, help_text="Blood Sugar=72-108 mg/dl", null=True)
    HB = models.CharField(max_length=30, help_text="Hemoglobin=13.0-16.0 g/dl", null=True)
    platelets = models.IntegerField(help_text="platelets=150,000–450,000", null=True)
    Prescription = models.CharField(max_length=500, null=True)

    def __str__(self):
        return '{} {} {} {}'.format(self.date, self.time, self.doctor, self.patient)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]

