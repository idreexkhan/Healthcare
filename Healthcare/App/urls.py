"""Healthcare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pat', views.pat, name='pat'),
    path('doc', views.doc, name='doc'),
    path('appointment/<str:user_id>', views.appointment, name='appointment'),
    path('register/', views.register, name='register'),
    path('patient_register/', views.patient_register.as_view(), name='patient_register'),
    path('doctor_register/', views.doctor_register.as_view(), name='doctor_register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('searchdoc', views.searchdoc, name='searchdoc'),
    path('apprecordpat', views.apprecordpat, name='apprecordpat'),
    path('appointment_chart', views.appointment_chart, name='appointment_chart'),
    path('addprescription/<str:id>', views.addprescription, name='addprescription'),
    path('addprescription/addprescriptiondoc/<str:id>', views.addprescriptiondoc, name='addprescriptiondoc'),
    path('diseaserec', views.diseaserec, name='diseaserec'),

]
