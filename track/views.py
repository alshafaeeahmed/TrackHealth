"""Views"""
from django.contrib import auth, messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.mail import send_mail, BadHeaderError

from . import forms, models


# home page
def home_view(request):
    """home page"""
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'index.html')


def adminclick_view(request):
    """admin click """
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the admin
    return render(request, 'adminclick.html')


def nurseclick_view(request):
    """nurse click """
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the nurse
    return render(request, 'nurseclick.html')


def nurse_feedback(request):
    """nurse feedback """
    nurse = models.Nurse.objects.get(user_id=request.user.id)
    feedback = models.Feedback()
    if request.method == 'POST':
        feedback.message = request.POST["message"]
        feedback.senderType = "nurse"
        feedback.by = request.user
        feedback.save()
        return render(request, 'feedback_for_nurse.html', {'nurse': nurse})
    return render(request, 'nurse_feedback.html', {'feedback': feedback, 'user': nurse})


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    """patient click """
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the patient
    return render(request, 'patientclick.html')


# check the type of the user
def is_admin(user):
    """check if user is admin """
    return user.is_staff


@user_passes_test(is_admin)
def admin_page(request):
    """admin page """
    context = {}
    nurses = models.Nurse.objects.all().count()
    patients = models.Patient.objects.all().count()
    context['patients'] = patients
    context['nurses'] = nurses
    return render(request, 'adminPage.html', context=context)


# nurse signup
def nurse_signup_view(request):
    """nurse signup """
    user_form = forms.NurseUserForm()
    nurse_form = forms.NurseForm()
    mydict = {'userForm': user_form, 'nurseForm': nurse_form}
    if request.method == 'POST':
        user_form = forms.NurseUserForm(request.POST)
        nurse_form = forms.NurseForm(request.POST, request.FILES)
        if user_form.is_valid() and nurse_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            nurse = nurse_form.save(commit=False)
            nurse.user = user
            nurse = nurse.save()
            my_nurse_group = Group.objects.get_or_create(name='NURSE')
            my_nurse_group[0].user_set.add(user)
        return HttpResponseRedirect('nurselogin')
    return render(request, 'nursesignup.html', context=mydict)


def is_nurse(user):
    """check if user in nurse """
    return user.groups.filter(name='NURSE').exists()


# patient signup
def patient_signup_view(request):
    """patient signup """
    user_form = forms.PatientUserForm()
    patient_form = forms.PatientForm()
    mydict = {'userForm': user_form, 'patientForm': patient_form}
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'patientsignup.html', context=mydict)


def aboutus(request):
    """about page """
    return render(request, "aboutus.html")


def contactus(request):
    """contactus page """
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject,
                          message,
                          'test.doctor.team22@gmail.com',
                          ['test.doctor.team22@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("home")

    form = forms.ContactForm()
    return render(request, "contact.html", {'form': form})


def afterlogin_view(request):
    """after login for users """
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    auth.login(request, user)
                    return redirect('admin-dashboard')
                if user is not None and user.groups.filter(name='NURSE').exists():
                    auth.login(request, user)
                    return redirect('nurse-dashboard')
                if user is not None and user.groups.filter(name='PATIENT').exists():
                    print("asdasdas")
                    auth.login(request, user)
                    return redirect('patient-dashboard')
                return None
            else:
                messages.info(request, 'invalid username or password')
                return redirect('login')
        else:
            return render(request, 'loginPage.html')
    else:
        if request.user.is_staff:
            return redirect('admin-dashboard')
        if request.user.groups.filter(name='NURSE'):
            return redirect('nurse-dashboard')
        if request.user.groups.filter(name='PATIENT'):
            return redirect('patient-dashboard')
    return None


@user_passes_test(is_nurse)
def nurse_dashboard(request):
    """nurse dashboard """
    mydict = {
    }
    return render(request, 'nurse_dashboard.html', context=mydict)


def is_patient(user):
    """check if user is patient """
    return user.groups.filter(name='PATIENT').exists()


@user_passes_test(is_patient)
def patient_dashboard(request):
    """patient dashboard """
    mydict = {}
    user = models.Patient.objects.get(user_id=request.user.id)
    # for i in models.Patient.objects.all():
    #     if i.user.id == user.id:
    mydict['user'] = user
    return render(request, 'patient_dashboard.html', context=mydict)


def logout_user(request):
    """logout for users """
    logout(request)
    return redirect('login')


@user_passes_test(is_admin)
def admin_patient_view(request):
    """admin show patients options """
    return render(request, 'admin_patient.html')


@user_passes_test(is_admin)
def admin_view_patient_view(request):
    """admin show all patients """
    patients = models.Patient.objects.all()
    return render(request, 'admin_view_patient.html', {'patients': patients})


@user_passes_test(is_admin)
def admin_view_report(request):
    """admin show nurse report """
    nurses = models.Nurse.objects.all()
    return render(request, 'admin_view_nurse_report.html', {'nurses': nurses})


@user_passes_test(is_nurse)
def nurse_view_patient(request):
    """nurse show all patients """
    patients = models.Patient.objects.all()
    dict = {}
    dict['patients'] = patients
    dict['user'] = models.Nurse.objects.get(user_id=request.user.id)
    return render(request, 'nurse_view_patients.html', context=dict)


@user_passes_test(is_nurse)
def nurse_report_view(request):
    """nurse show all patients to write report"""
    patients = models.Patient.objects.all()
    dict = {}
    dict['patients'] = patients
    dict['user'] = models.Nurse.objects.get(user_id=request.user.id)
    return render(request, 'nurse_report.html', context=dict)


def nurse_report(request, id_):
    """nurse add report """
    dect = {}
    dect['records'] = models.Record.objects.filter(nurse_id=id_)
    return render(request, 'admin_nurse_report.html', dect)


@user_passes_test(is_admin)
def admin_nurse_view(request):
    """admin show all nurses """
    patients = models.Patient.objects.all()
    return render(request, 'admin_nurse.html', {'patients': patients})


def update_urine_surgery(request, id_):
    """nurse update Urine Surgery """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Urine_surgery = request.POST['UrineSurgery']
        user.save()
    return render(request, 'updateUrineSurgery.html')


@user_passes_test(is_admin)
def admin_add_nurse(request):
    """admin add nurse user """
    user_form = forms.NurseUserForm()
    nurse_form = forms.NurseForm()
    mydict = {'userForm': user_form, 'nurseForm': nurse_form}
    if request.method == 'POST':
        user_form = forms.NurseUserForm(request.POST)
        nurse_form = forms.NurseForm(request.POST, request.FILES)
        if user_form.is_valid() and nurse_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            nurse = nurse_form.save(commit=False)
            nurse.user = user
            nurse.save()
            my_nurse_group = Group.objects.get_or_create(name='NURSE')
            my_nurse_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-nurse')
    return render(request, 'admin_add_nurse.html', context=mydict)


# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient(request):
    """admin add patient user """
    user_form = forms.PatientUserForm()
    patient_form = forms.PatientForm()
    mydict = {'userForm': user_form, 'patientForm': patient_form}
    if request.method == 'POST':
        user_form = forms.PatientUserForm(request.POST)
        patient_form = forms.PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            print("|Asdasdaddas")
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-patient')
    return render(request, 'admin_add_patient.html', context=mydict)


@user_passes_test(is_nurse)
def nurse_food(request):
    """nurse food options """
    dict = {}
    dict['user'] = models.Nurse.objects.get(user_id=request.user.id)
    return render(request, 'nurse_food.html', context=dict)


@user_passes_test(is_patient)
def patient_feedback(request):
    """patient send message to admin """
    if request.method == 'POST':
        feedback = models.Feedback()
        feedback.by = request.user
        feedback.message = request.POST['message']
        feedback.senderType = "Patient"
        feedback.sen_id = request.user.id
        feedback.save()
        # patient = models.Patient()
        # for i in models.Patient.objects.all():
        #     if request.user == i.user:
        #         patient = i
        return render(request, 'feedback_for_patient.html')
    return render(request, 'patient_feedback.html')


@user_passes_test(is_nurse)
def update_ecg(request, id_):
    """nurse update ECG test """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.ECG = request.POST['ECG']
        user.save()
    return render(request, 'updateECG.html')


@user_passes_test(is_admin)
def admin_feedbacks(request):
    """admin show all feedback users """
    feedback = models.Feedback.objects.all().order_by('-id')
    return render(request, 'admin_feedbacks.html', {'feedback': feedback})


@user_passes_test(is_admin)
def admin_replay(request, id_):
    """admin send replay to patient message """
    feedback = models.Feedback.objects.all().get(id=id_)
    if request.method == 'POST':
        feedback.replay = request.POST['replay']
        feedback.save()
        return render(request, 'replay_for_admin.html')
    return render(request, 'admin_replay.html')


@user_passes_test(is_nurse)
def nurse_message(request, id_):
    """nurse send message to admin """
    patient = None
    for i in models.Patient.objects.all():
        if i.user_id == id_:
            patient = i
    print(patient)
    if request.method == 'POST':
        message = models.Feedback()
        message.by = request.user.username
        message.message = request.POST['message']
        message.senderType = "Nurse"
        message.sen_id = request.user.id
        message.rec_id = patient.user_id
        message.save()
        # patient.feedbacks.add(message)
        return render(request, 'message_for_nurse.html')
    return render(request, 'nurseMessage.html', {'user': request.user})


@user_passes_test(is_patient)
def feedback_list(request):
    """patient show messages that he sent """
    context = {}
    if request.user.is_authenticated and not request.user.is_anonymous:
        for i in models.Patient.objects.all():
            if request.user.id == i.user_id:
                context['feedbacks'] = models.Feedback.objects.filter(sen_id=i.user_id)
        return render(request, 'patient_feedbacks.html', context)
    return None


@user_passes_test(is_patient)
def message_list(request):
    """patient show messages with replays """
    context = {}
    if request.user.is_authenticated and not request.user.is_anonymous:
        for i in models.Patient.objects.all():
            if request.user.id == i.user_id:
                context['feedbacks'] = models.Feedback.objects.filter(rec_id=i.user_id)
        return render(request, 'patient_received.html', context)
    return None


@user_passes_test(is_patient)
def profile(request):
    """patient profile """
    mydict = {}
    user = models.User.objects.get(id=request.user.id)
    for i in models.Patient.objects.all():
        if i.user_id == user.id:
            mydict['user'] = i
    return render(request, 'profile.html', mydict)


@user_passes_test(is_nurse)
def update_blood_pressure(request, id_):
    """nurse update Blood Pressure """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Blood_Pressure = request.POST['BloodPressure']
        user.save()
    return render(request, 'updateBloodPressure.html')


@user_passes_test(is_patient)
def update_blood_pressure_patient(request, id_):
    """patient update Blood Pressure """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Blood_Pressure = request.POST['BloodPressure']
        user.save()
    return render(request, 'updateBloodPressurePatient.html')


def nurse_profile(request):
    user = models.Nurse.objects.get(user_id=request.user.id)
    return render(request, 'nurseprofile.html', {'user': user})


@user_passes_test(is_nurse)
def update_cholesterol(request, id_):
    """nurse update Cholesterol """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Cholesterol = request.POST['Cholesterol']
        user.save()
    return render(request, 'updateCholesterol.html')


@user_passes_test(is_nurse)
def update_fats(request, id_):
    """nurse update Fats """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Fats = request.POST['Fats']
        user.save()
    return render(request, 'updateFats.html')


def update_liver_function(request, id_):
    """nurse update Liver Function """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Liver_function = request.POST['LiverFunction']
        user.save()
    return render(request, 'updateLiverFunction.html')


def update_kidney_function(request, id_):
    """nurse update Kidney Function """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Kidney_function = request.POST['KidneyFunction']
        user.save()
    return render(request, 'updateKidneyFunction.html')


@user_passes_test(is_patient)
def patient_view_food(request):
    """patient show food list """
    food = models.Food.objects.all()
    return render(request, 'patient_view_food.html', {'food': food})


@user_passes_test(is_patient)
def show_food_list(request):
    """patient show food list that he selected """
    context = None
    lst = []
    if request.user.is_authenticated and not request.user.is_anonymous:
        user_info = models.Patient.objects.get(user=request.user)
        food = models.FoodPatient.objects.filter(patient_id=user_info.user_id)
        for i in food:
            for j in models.Food.objects.all():
                if i.foodName == j.Name:
                    lst.append(j)
        context = {'food': lst}
        print(lst)
        print(user_info.user)
    return render(request, 'show_food_list.html', context)


@user_passes_test(is_patient)
def food_list(request, id_):
    """check the food that the patient is selected """
    patient = models.Patient.objects.get(user=request.user)
    f = models.FoodPatient()
    for i in models.Food.objects.all():
        if i.Name == id_:
            print("TTTTrue")
            food = i
            f.foodName = food.Name
    check = patient.Cholesterol > food.max_Cholesterol or patient.Liver_function > food.max_Liver_function or patient.Kidney_function > food.max_Kidney_function or patient.Blood_Pressure > food.max_Blood_Pressure
    if request.user.is_authenticated and not request.user.is_anonymous:
        if check is not True:
            messages.error(request, '\t')
        if check is True:
            print("True")
            user = models.Patient.objects.get(user=request.user)
            food.patient_id = user.user_id
            f.patient_id = user.user_id
            f.save()
            messages.success(request, '\t')
    else:
        redirect('')
    return redirect('patient-view-food')


@user_passes_test(is_nurse)
def nurse_view_food(request):
    """nurse show food list """
    food = models.Food.objects.all()
    dict = {}
    dict['user'] = models.Nurse.objects.get(user_id=request.user.id)
    dict['food'] = food
    return render(request, 'nurse_view_food.html', context=dict)


@user_passes_test(is_nurse)
def delete_food(id_):
    """nurse delete food from list """
    print("asdasdasdasd")
    for i in models.Food.objects.all():
        if i.Name == id_:
            print("asdasdasd")

    # for i in food:
    #     if i.Name==pk:
    #         i.delete()
    # print(i.max_Blood_Pressure)
    # print(models.Food.objects.filter(Name=pk))
    # print(food.max_Cholesterol)
    # for i in models.Food.objects.all():
    #     if i.Name == pk:
    #         i.delete()
    return HttpResponseRedirect('/nurse-view-food')


@user_passes_test(is_nurse)
def nurse_add_food(request):
    """nurse add food to list """
    flag = False
    dict = {}
    dict['user'] = models.Nurse.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        food = models.Food()
        for i in models.Food.objects.all():
            if i.Name == request.POST['Name']:
                flag = True

        food.Name = request.POST['Name']
        food.number = request.POST['num']
        food.max_Cholesterol = request.POST['max_Cholesterol']
        food.max_Liver_function = request.POST['max_Liver_function']
        food.max_Kidney_function = request.POST['max_Kidney_function']
        food.max_Blood_Pressure = request.POST['max_Blood_Pressure']
        food.pic = request.FILES['pic']
        if flag is False:
            food.save()
        else:
            messages.error(request, "The role is already booked")

        return HttpResponseRedirect('nurse-dashboard')
    return render(request, 'nurse_add_food.html', context=dict)


# BSPM2022T1
@user_passes_test(is_admin)
def admin_add_medication(request, id_patient):
    """admin add medication for patient """
    if request.method == 'POST':
        medication = models.Medication()
        medication.name = request.POST['name']
        medication.numOftimes = request.POST['numOftimes']
        medication.mg = request.POST['mg']
        medication.expiratDate = request.POST['expiratDate']
        medication.Description = request.POST['Description']
        medication.patient_id = id_patient
        medication.save()
        return render(request, 'admin_view_patient.html',
                      context={'patients': models.Patient.objects.all()}
                      )
    return render(request, 'admin_add_medication.html')


@user_passes_test(is_nurse)
def nurse_add_record(request, id_nurse):
    """nurse add record """
    dict = {}
    dict['patients'] = models.Patient.objects.all()
    dict['user'] = models.Nurse.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        record = models.Record()
        record.patientName = request.POST['patientName']
        record.body = request.POST['body']
        record.nurse_id = id_nurse
        record.save()
        return render(request, 'nurse_Record.html')
    return render(request, 'nurse_Record.html', context=dict)


def update_glucose(request, id_):
    """nurse update Glucose """
    if request.method == 'POST':
        user = models.Patient.objects.get(user_id=id_)
        user.Glucose = request.POST['Glucose']
        user.save()
    return render(request, 'updateGlucose.html')


@user_passes_test(is_patient)
def show_medication_list(request):
    """patient show medication list that doctor adds"""
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        user_info = models.Patient.objects.get(user=request.user)
        medication = models.Medication.objects.filter(patient_id=user_info.user_id)
        context = {'medication': medication}
    return render(request, 'show_medication_list.html', context)


def appointment_patient(request):
    """patient Appointment options """
    return render(request, 'patient_appointment.html')


def admin_book_appointment(request):
    """admin book appointment for the patient """
    patient = models.Patient()
    if request.method == 'POST':
        check = False
        for i in models.Patient.objects.all():
            if i.user.username == request.POST['patientName']:
                check = True
                patient = i
        if check:
            appointment = models.Appointment()
            appointment.date = request.POST['appointment']
            appointment.time = request.POST['time']
            appointment.name = patient.user
            appointment.patient_id = patient.user_id
            flag = True
            for i in models.Appointment.objects.all():
                if (str(i.date) == str(appointment.date)
                        and str(i.time)[0:5] == str(appointment.time)):
                    flag = False
                    messages.error(request, "The role is already booked")
            if flag:
                appointment.save()

                messages.success(request, "Book Success")
    return render(request, 'AdminBookAppointment.html', {'patients': models.Patient.objects.all()})


def patient_appointments(request):
    """patient show appointments """
    context = {}
    context['appointment'] = models.Appointment.objects.filter(patient_id=request.user.id)
    return render(request, 'MyAppointment.html', context)


def admin_appointments(request):
    """admin appointments option """
    appointments = models.Appointment.objects.all()
    return render(request, 'adminAppointments.html', {'appointments': appointments})


def book_appointment(request):
    """patient Book Appointment """
    if request.method == 'POST':
        appointment = models.Appointment()
        appointment.date = request.POST['appointment']
        appointment.time = request.POST['time']
        appointment.name = request.user.username
        appointment.patient_id = request.user.id
        flag = True
        for i in models.Appointment.objects.all():
            if (str(i.date) == str(appointment.date) and
                    str(i.time)[0:5] == str(appointment.time)[0:5]):
                flag = False
                messages.error(request, "The role is already booked")
        if flag:
            appointment.save()
            messages.success(request, "Book Success")
    return render(request, 'BookAppointment.html')


def admin_appointment(request):
    """admin Appointment option """
    return render(request, 'admin_appointment.html')


@user_passes_test(is_patient)
def map_view(request):
    """map for patient to find Pharmacy """
    return render(request, 'map.html')
