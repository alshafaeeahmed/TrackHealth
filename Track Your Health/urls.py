"""Track Your Health URL Configuration

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from track import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),
    path('home', views.home_view, name='home'),

    path('adminclick', views.adminclick_view),
    path('nurseclick', views.nurseclick_view),
    path('patientclick', views.patientclick_view),


    #signup urls
    path('adminlogin', LoginView.as_view(template_name='loginPage.html')),

    path('nursesignup', views.nurse_signup_view, name='nursesignup'),

    path('login', views.afterlogin_view, name='login'),


    path('aboutus', views.aboutus, name='aboutus'),
    path('contactus', views.contactus, name='contactus'),

    path('nurse-dashboard', views.nurse_profile, name='nurse-dashboard'),
    path('admin-dashboard', views.admin_page, name='admin-dashboard'),

    path('adminlogin', LoginView.as_view(template_name='loginPage.html')),
    path('nurselogin', LoginView.as_view(template_name='loginPage.html')),
    path('patientlogin', LoginView.as_view(template_name='loginPage.html')),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('patientsignup', views.patient_signup_view),
    path('patient-dashboard', views.patient_dashboard, name='patient-dashboard'),

    path('patient-dashboard/<int:id>', views.patient_dashboard, name='patient-dashboard'),
    path('logout', views.logout_user, name='logout'),

    path('patient-feedback', views.patient_feedback, name='patient-feedback'),
    path('nurse-feedback', views.nurse_feedback, name='nurse-feedback'),
    path('admin-feedbacks', views.admin_feedbacks, name='admin-feedbacks'),
    path('nurse-message/<int:id_>', views.nurse_message, name='nurse-message'),
    path('patient-replays', views.feedback_list, name='patient-replays'),
    path('patient-messages', views.message_list, name='patient-messages'),
    path('send-replay/<int:id_>', views.admin_replay, name='send-replay'),
    path('patient-view-food', views.patient_view_food, name='patient-view-food'),
    path('food-favorite/<str:id_>', views.food_list, name='food-favorite'),
    path('show-food-list', views.show_food_list, name='show-food-list'),
    path('show-medication-list', views.show_medication_list, name='show-medication-list'),
    path('appointment', views.appointment_patient, name='appointment'),
    path('My-Appointment', views.patient_appointments, name='My-Appointment'),
    path('bookappointment', views.book_appointment, name='bookappointment'),

    path('profile/', views.profile, name='users-profile'),
    path('nurseprofile/', views.nurse_profile, name='nurseprofile'),
    path('update-BloodPressurePatient/<int:id_>', views.update_blood_pressure_patient, name='update-BloodPressurePatient'),
    path('update-BloodPressure/<int:id_>', views.update_blood_pressure, name='update-BloodPressure'),
    path('update-ECG/<int:id_>', views.update_ecg, name='update-ECG'),
    path('update-Glucose/<int:id_>', views.update_glucose, name='update-Glucose'),
    path('update-LiverFunction/<int:id_>', views.update_liver_function, name='update-LiverFunction'),
    path('update-KidneyFunction/<int:id_>', views.update_kidney_function, name='update-KidneyFunction'),
    path('update-Cholesterol/<int:id_>', views.update_cholesterol, name='update-Cholesterol'),
    path('update-Fats/<int:id>', views.update_fats, name='update-Fats'),

    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view, name='admin-view-patient'),
    path('admin-view-report', views.admin_view_report, name='admin-view-report'),
    path('admin-nurse', views.admin_nurse_view, name='admin-nurse'),
    path('admin-add-nurse', views.admin_add_nurse, name='admin-add-nurse'),
    path('admin-add-patient', views.admin_add_patient, name='admin-add-patient'),
    path('adminAppointment', views.admin_appointment, name='adminAppointment'),
    path('adminbookappointment', views.admin_book_appointment, name='adminbookappointment'),
    path('admin-appointments', views.admin_appointments, name='admin-appointments'),

    path('nurse-food', views.nurse_food, name='nurse-food'),
    path('nurse-add-food', views.nurse_add_food, name='nurse-add-food'),
    path('nurse-patient', views.nurse_view_patient, name='nurse-patient'),
    path('nurse-reprot', views.nurse_report_view, name='nurse-reprot'),
    path('admin-nurse-reprot/<int:id_>', views.nurse_report, name='admin-nurse-reprot'),
    path('update-Urine-surgery/<int:id_>', views.update_urine_surgery, name='update-Urine-surgery'),
    path('admin-add-medication/<int:id_patient>', views.admin_add_medication, name='admin-add-medication'),
    path('nurse-add-record/<int:id_nurse>', views.nurse_add_record, name='nurse-add-record'),
    path('nurse-view-food', views.nurse_view_food, name='nurse-view-food'),
    path('delete-food/<str:id_>', views.delete_food, name='delete-food'),


    path('map', views.map_view, name='map'),
]
