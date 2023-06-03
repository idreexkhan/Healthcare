from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.views.generic import CreateView
from .forms import PatientSignUpForm, DoctorSignUpForm, AppointmentForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Doctor, Patient, Appointment
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
import datetime
import collections


@cache_page(60 * 15)
@csrf_protect
def index(request):
    return render(request, 'index.html')


def pat(request):
    patt = request.user.id
    apps = Appointment.objects.filter(Q(patient_id=patt) & Q(date=datetime.date.today()))

    context = {
        'apps': apps,
    }
    return render(request, 'pat.html', context)


def doc(request):
    doct = request.user.id
    apps = Appointment.objects.filter(Q(doctor_id=doct) & Q(date=datetime.date.today()))
    context = {
        'apps': apps,
    }
    return render(request, 'doc.html', context)


def register(request):
    return render(request, 'register.html')


class doctor_register(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'doctor_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class patient_register(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'patient_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request, user=None):
    try:
        if user.is_authenticated:
            if user.is_doctor:
                return render(request, 'doc.html')
            else:
                return render(request, 'pat.html')

    except:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_doctor:
                        return render(request, 'doc.html')
                    else:
                        return render(request, 'pat.html')
            else:
                messages.error(request, "Invalid username or password")
        return render(request, 'login.html',
                      context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


def searchdoc(request):
    if request.method == "POST":
        specialization = request.POST['specialization']

        docs = Doctor.objects.filter(specialization__icontains=specialization)

        context = {
            'docs': docs,
        }
        return render(request, 'searchdoc.html', context)

    elif request.method == 'GET':
        return render(request, 'searchdoc.html')
    else:
        return HttpResponse("An Exception Occurred")


def apprecordpat(request):
    patt = request.user.id
    recs = Appointment.objects.filter(patient_id=patt)

    context = {
        'recs': recs,
    }
    return render(request, 'apprecordpat.html', context)


def appointment(request, user_id):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctordata = Doctor.objects.get(user=user_id)
            patientdata = Patient.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.doctor = doctordata
            instance.patient = patientdata
            instance.save()
            messages.success(request, 'appointment booked successfully')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})


def appointment_chart(request):
    docid = request.user.id
    dat = datetime.date.today()
    dat = dat.month
    data = []
    total_appointment = Appointment.objects.filter(doctor_id=docid).filter(date__month=dat).count()

    data.append(total_appointment)

    data = {
        'data': data,
    }
    return render(request, 'appointment_chart.html', data)


def addprescription(request, id):
    app = Appointment.objects.get(id=id)
    template = loader.get_template('addprescription.html')
    context = {
        'app': app,
    }
    return HttpResponse(template.render(context, request))


def addprescriptiondoc(request, id):
    Prescription = request.POST['Prescription']
    app = Appointment.objects.get(id=id)
    app.Prescription = Prescription
    app.save()
    return HttpResponse("Prescription Added Successfully")


def diseaserec(request):
    docid = request.user.id
    dat = datetime.date.today()
    dat = dat.month
    disrec = Appointment.objects.filter(doctor_id=docid).filter(date__month=dat).values_list('disease')
    total = dict(collections.Counter(disrec))
    context = {
        'total': total,
    }
    print(total)
    return render(request, "diseaserec.html", context)
