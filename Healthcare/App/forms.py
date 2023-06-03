from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Patient, Doctor, Appointment
from datetimewidget.widgets import DateTimeWidget


class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    age = forms.IntegerField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        patient = Patient.objects.create(user=user)
        patient.phone_number = self.cleaned_data.get('phone_number')
        patient.age = self.cleaned_data.get('age')
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    Qualification = forms.CharField(required=True)
    specialization = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.phone_number = self.cleaned_data.get('phone_number')
        doctor.Qualification = self.cleaned_data.get('Qualification')
        doctor.specialization = self.cleaned_data.get('specialization')
        doctor.save()
        return user


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('disease', 'BP', 'BMI', 'BS', 'HB', 'platelets', 'date', 'timeslot')
        widgets = {
            'date': DateTimeWidget(
                attrs={'id': 'date'}, usel10n=False, bootstrap_version=3,
                options={
                    'minView': 2,  # month view
                    'maxView': 3,  # year view
                    'weekStart': 1,
                    'todayHighlight': True,
                    'format': 'yyyy/mm/dd',
                    'daysOfWeekDisabled': [7],
                    'startDate': date.today().strftime('%y-%m-%d'),
                }),

        }

    def clean_date(self):
        day = self.cleaned_data['date']

        if day <= date.today():
            raise forms.ValidationError('Date should be upcoming (tomorrow or later)', code='invalid')
        if day.isoweekday() in (0, 7):
            raise forms.ValidationError('Day should be a workday', code='invalid')

        return day
