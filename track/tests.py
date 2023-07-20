"""Unit Test And Integration Test """
import unittest
from django.test import tag
from django.urls import reverse
from django.test import Client
from track.models import User


@tag("unit_test")
class LogoutTest(unittest.TestCase):
    """LogoutTest """
    client = Client()

    def test_logout(self):
        """testLogout """
        self.client.login(username='username', password='password')

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)



#
@tag("unit_test")
class AdminPatientFormTests(unittest.TestCase):
    """AdminPatientFormTests """
    client = Client()

    @tag('unit-test')
    def test_add_patient_get(self):
        """test_add_patient_get """
        response = self.client.get(reverse('admin-add-patient'))
        self.assertNotEqual(response.status_code, 300)


@tag("unit_test")
class AdminNurseFormTests(unittest.TestCase):
    """AdminNurseFormTests """
    client = Client()


    @tag("unit-test")
    def test_add_nurse_get(self):
        """test_add_nurse_get """
        client = Client()
        response = client.get(reverse('admin-add-nurse'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_login(self):
        """test_login """
        client = Client()
        login = client.login(username='test', password='test')
        self.assertFalse(login)


@tag('unit-test')
class RegisterTestNurse(unittest.TestCase):
    """RegisterTest_Nurse """
    client = Client()

    @tag('unit-test')
    def test_register_access_url(self):
        """test_register_access_url """
        response = self.client.get('/nursesignup')
        self.assertEqual(response.status_code, 200)


class RegisterTestPatient(unittest.TestCase):
    """RegisterTest_Patient """
    client = Client()

    @tag('unit-test')
    def test_register_access_url(self):
        """test_register_access_url """
        response = self.client.get('/patientsignup')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_register_access_name(self):
        """test_register_access_name """
        response = self.client.get('patientsignup')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_register_access_url_negative(self):
        """test_register_access_url_negative """
        response = self.client.get('patientsignup')
        self.assertNotEqual(response.status_code, 300)


class LoginTest(unittest.TestCase):
    """loginTest """
    client = Client()

    @tag('unit-test')
    def test_login_access_url(self):
        """test_login_access_url """
        response = self.client.get('/login/')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_login_access_name(self):
        """test_login_access_name """
        response = self.client.get(reverse('login'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_login_access_url_negative(self):
        """test_login_access_url_negative """
        response = self.client.get('/login/')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_login_access_name_negative(self):
        """test_login_access_name_negative """
        response = self.client.get(reverse('login'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_login_used_template(self):
        """test_login_used_template """
        response = self.client.get(reverse('login'))
        self.assertNotEqual(response.status_code, 300)
        value = 'loginPage.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_login_not_used_template(self):
        """test_login_not_used_template """
        response = self.client.get(reverse('login'))
        self.assertNotEqual(response.status_code, 300)
        value = 'home.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_user_login(self):
        """test_user_login """
        data = {'username': 'a12', 'password': '1234'}
        response = self.client.post(reverse('login'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(reverse('login'))

    @tag('integration-test')
    def test_login_and_logout(self):
        """test_login_and_logout """
        data = {'username': 'a12', 'password': '1234'}
        response = self.client.post(reverse('login'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        value = 'loginPage.html'
        self.assertTrue(response, value)

        response = self.client.get(reverse('logout'), follow=True)

        # Assert
        self.assertNotEqual(response.status_code, 300)
        self.assertFalse(response.context["user"].is_authenticated)


class FeedbackTest(unittest.TestCase):
    """FeedbackTest """
    client = Client()

    @tag('unit-test')
    def test_feedback_access_url(self):
        """test_feedback_access_url """
        response = self.client.get('patient-feedback', )
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_feedback_access_subject(self):
        """test_feedback_access_subject """
        response = self.client.get(reverse('patient-feedback'))
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_feedback_access_url_negative(self):
        """test_feedback_access_url_negative """
        response = self.client.get('/patient-feedback')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_view(self):
        """test_view """
        data = {'feedbackContent': 'content', }
        response = self.client.post(reverse('patient-feedback'), data=data, follow=True)
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_admin_feedbacks_access_url(self):
        """test_admin_feedbacks_access_url """
        response = self.client.get('/admin-feedbacks')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_admin_feedbacks_access_template(self):
        """test_admin_feedbacks_access_template """
        data = {'feedbackContent': 'content', }
        response = self.client.post(reverse('admin-feedbacks'), data=data, follow=True)
        self.assertNotEqual(response.status_code, 300)
        value = 'admin_feedbacks.html'
        self.assertTrue(response, value)


class AddMedicationTest(unittest.TestCase):
    """addMedicationTest """
    client = Client()

    @tag('unit-test')
    def test_medication_access_url(self):
        """test_medication_access_url """
        response = self.client.get('/admin-add-medication')
        self.assertNotEqual(response.status_code, 300)


class AddRecordTest(unittest.TestCase):
    """addRecordTest """
    client = Client()

    @tag('unit-test')
    def test_record_access_url(self):
        """test_record_access_url """
        response = self.client.get('/nurse-add-record')
        self.assertNotEqual(response.status_code, 300)


class AddFoodTest(unittest.TestCase):
    """addFoodTest """
    client = Client()

    @tag('unit-test')
    def test_food_access_url(self):
        """test_food_access_url """
        response = self.client.get('/nurse-add-food')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_food_access_template(self):
        """test_food_access_template """
        response = self.client.get(('/nurse-add-food'))
        self.assertNotEqual(response.status_code, 300)
        value = 'nurse_add_food.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_add_to_food_list(self):
        """test_add_to_food_list """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('nurse-add-food'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class ViewFoodTest(unittest.TestCase):
    """viewFoodTest """
    client = Client()

    @tag('unit-test')
    def test_food_view_template(self):
        """test_food_view_template """
        response = self.client.get('/patient-view-food')
        self.assertNotEqual(response.status_code, 300)


# ########## Hackathon Unit Test

class NurseMessageTest(unittest.TestCase):
    """NurseMessageTest """
    client = Client()

    @tag('unit-test')
    def test_message_access_url(self):
        """test_message_access_url """
        response = self.client.get('nurse-message')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_message_access_template(self):
        """test_message_access_template """
        response = self.client.get(('nurse-message'))
        self.assertNotEqual(response.status_code, 300)
        value = 'nurseMessage.html'
        self.assertTrue(response, value)


class NurseInsertTest(unittest.TestCase):
    """NurseInsertTest """
    client = Client()

    @tag('unit-test')
    def test_liver_function_access_url(self):
        """test_liver_function_access_url """
        response = self.client.get('update-LiverFunction/<int:id>')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_liver_function_access_template(self):
        """test_liver_function_access_template """
        response = self.client.get('update-LiverFunction/<int:id>')
        self.assertNotEqual(response.status_code, 300)
        self.assertTrue(response, 'updateLiverFunction.html')


class DashboardUsersTest(unittest.TestCase):
    """DashboardUsersTest """
    client = Client()

    @tag('unit-test')
    def test_admin_dashboard_access_url(self):
        """test_admin_dashboard_access_url """
        response = self.client.get('admin-dashboard')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_admin_dashboard_access_template(self):
        """test_admin_dashboard_access_template """
        response = self.client.get('admin-dashboard')
        self.assertNotEqual(response.status_code, 300)
        value = 'admin_dashboard.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_admin_dashboard(self):
        """test_admin_dashboard """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('admin-dashboard'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_patient_dashboard_access_url(self):
        """test_patient_dashboard_access_url """
        response = self.client.get('patient-dashboard')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_patient_dashboard_access_template(self):
        """test_patient_dashboard_access_template """
        response = self.client.get('patient-dashboard')
        self.assertNotEqual(response.status_code, 300)
        value = 'patient_dashboard.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_patient_dashboard(self):
        """test_patient_dashboard """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('patient-dashboard'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_nurse_dashboard_access_url(self):
        """test_nurse_dashboard_access_url """
        response = self.client.get('nurse-dashboard')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_nurse_dashboard_access_template(self):
        """test_nurse_dashboard_access_template """
        response = self.client.get('nurse-dashboard')
        self.assertNotEqual(response.status_code, 300)
        value = 'nurse_dashboard.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_nurse_dashboard(self):
        """test_nurse_dashboard """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('nurse-dashboard'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class UpdateECGTest(unittest.TestCase):
    """UpdateECGTest """
    client = Client()

    @tag('unit-test')
    def test_update_ecg_access_url(self):
        """test_update_ecg_access_url """
        response = self.client.get('update-ECG')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_update_ecg_access_template(self):
        """test_update_ecg_access_template """
        response = self.client.get('update-ECG')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateECG.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_update_ecg(self):
        """test_update_ecg """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('update-ECG'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class UpdateInfoTest(unittest.TestCase):
    """UpdateInfoTest """
    client = Client()

    @tag('unit-test')
    def test_update_glucose_access_url(self):
        """test_update_glucose_access_url """
        response = self.client.get('update-Glucose')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_update_glucose_access_template(self):
        """test_update_glucose_access_template """
        response = self.client.get('update-Glucose')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateGlucose.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_update_glucose(self):
        """test_update_glucose """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('update-Glucose'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)

    @tag('unit-test')
    def test_blood_pressure_patient_access_url(self):
        """test_blood_pressure_patient_access_url """
        response = self.client.get('update-BloodPressurePatient')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_blood_pressure_patient_access_template(self):
        """test_blood_pressure_patient_access_template """
        response = self.client.get('update-BloodPressurePatient')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateBloodPressurePatient.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_blood_pressure_patient(self):
        """test_blood_pressure_patient """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('update-BloodPressurePatient'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class NurseInsertInfoTest(unittest.TestCase):
    """NurseInsertInfoTest """

    client = Client()

    @tag('unit-test')
    def test_fats_access_url(self):
        """test_fats_access_url """
        response = self.client.get('update-Fats/<int:id>')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_fats_access_template(self):
        """test_fats_access_template """
        response = self.client.get('update-Fats/<int:id>')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateFats.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_cholesterol_access_url(self):
        """test_cholesterol_access_url """
        response = self.client.get('update-Cholesterol/<int:id>')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_cholesterol_access_template(self):
        """test_cholesterol_access_template """
        response = self.client.get('update-Cholesterol/<int:id>')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateCholesterol.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_blood_pressure_access_url(self):
        """test_blood_pressure_access_url """
        response = self.client.get('update-BloodPressure/<int:id>')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_blood_pressure_access_template(self):
        """test_blood_pressure_access_template """
        response = self.client.get('update-BloodPressure/<int:id>')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateBloodPressure.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_kidney_function_access_url(self):
        """test_kidney_function_access_url """
        response = self.client.get('update-KidneyFunction/<int:id>')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_kidney_function_access_template(self):
        """test_kidney_function_access_template """
        response = self.client.get('update-KidneyFunction/<int:id>')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateKidneyFunction.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_login_and_logout(self):
        """test_login_and_logout """
        # Login
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        self.assertNotEqual(response.status_code, 300)

        # logout
        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)

    @tag('integration-test')
    def test_update_kidney_function(self):
        """test_update_kidney_function """
        # accss view
        self.assertTrue(User.is_authenticated)
        response = self.client.get(('update-KidneyFunction/<int:id>'))

        self.assertNotEqual(response.status_code, 300)

        # logout
        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class PatientBookAppointmentTest(unittest.TestCase):
    """PatientBookAppointmentTest """
    client = Client()

    @tag('unit-test')
    def test_appointment_access_url(self):
        """test_appointment_access_url """
        response = self.client.get('appointment')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_book_appointment_access_url(self):
        """test_book_appointment_access_url """
        response = self.client.get('bookappointment')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_book_appointment_access_template(self):
        """test_book_appointment_access_template """
        response = self.client.get('bookappointment')
        self.assertNotEqual(response.status_code, 300)
        value = 'BookAppointment.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_appointment_access_template(self):
        """test_appointment_access_template """
        response = self.client.get('appointment')
        self.assertNotEqual(response.status_code, 300)
        value = 'patient_appointment.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_login_and_patient_book_appointment_and_logout(self):
        """test_login_and_patient_book_appointment_and_logout """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('bookappointment'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class AdminBookAppointmentTest(unittest.TestCase):
    """AdminBookAppointmentTest """
    client = Client()

    @tag('unit-test')
    def test_admin_book_appointment_access_url(self):
        """test_admin_book_appointment_access_url """
        response = self.client.get('adminAppointment')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_admin_appointment_access_url(self):
        """test_admin_appointment_access_url """
        response = self.client.get('adminbookappointment')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_admin_book_appointment_access_template(self):
        """test_admin_book_appointment_access_template """
        response = self.client.get('adminbookappointment')
        self.assertNotEqual(response.status_code, 300)
        value = 'AdminBookAppointment.html'
        self.assertTrue(response, value)

    @tag('unit-test')
    def test_admin_appointment_access_template(self):
        """test_admin_appointment_access_template """
        response = self.client.get('appointment')
        self.assertNotEqual(response.status_code, 300)
        value = 'admin_appointment.html'
        self.assertTrue(response, value)

    @tag('integration-test')
    def test_login_and_admin_book_appointment_and_logout(self):
        """test_login_and_admin_book_appointment_and_logout """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('adminbookappointment'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class PatientMapTest(unittest.TestCase):
    """PatientMapTest """
    client = Client()

    @tag('unit-test')
    def test_map_access_url(self):
        """test_map_access_url """
        response = self.client.get('map')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_map_access_template(self):
        """test_map_access_template """
        response = self.client.get('map')
        self.assertNotEqual(response.status_code, 300)
        value = 'map.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_map(self):
        """test_map """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('map'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class NurseAddRecordTest(unittest.TestCase):
    """NurseAddRecordTest """
    client = Client()

    @tag('unit-test')
    def test_record_access_url(self):
        """test_record_access_url """
        response = self.client.get('admin-nurse-reprot')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_record_access_template(self):
        """test_record_access_template """
        response = self.client.get('admin-nurse-reprot')
        self.assertNotEqual(response.status_code, 300)
        value = 'nurse_Record.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_nurse_add_record(self):
        """test_nurse_add_record """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('admin-nurse-reprot'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class UpdateUrineSurgeryTest(unittest.TestCase):
    """UpdateUrineSurgeryTest """
    client = Client()

    @tag('unit-test')
    def test_urine_surgery_access_url(self):
        """test_urine_surgery_access_url """
        response = self.client.get('update-Urine-surgery')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_urine_surgery_access_template(self):
        """test_urine_surgery_access_template """
        response = self.client.get('update-Urine-surgery')
        self.assertNotEqual(response.status_code, 300)
        value = 'updateUrineSurgery.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_urine_surgery(self):
        """test_urine_surgery """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('update-Urine-surgery'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class PatientMedicationList(unittest.TestCase):
    """PatientMedicationList """
    client = Client()

    @tag('unit-test')
    def test_medication_list_access_url(self):
        """test_medication_list_access_url """
        response = self.client.get('show-medication-list')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_medication_list_access_template(self):
        """test_medication_list_access_template """
        response = self.client.get('show-medication-list')
        self.assertNotEqual(response.status_code, 300)
        value = 'show_medication_list.html'
        self.assertTrue(value)

    @tag('integration-test')
    def test_medication_list(self):
        """test_medication_list """
        # accss view
        response = self.client.get(('login'))
        self.assertTrue(User.is_authenticated)

        response = self.client.get(('show-medication-list'))
        self.assertNotEqual(response.status_code, 300)

        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)


class PatientUserProfile(unittest.TestCase):
    """PatientUserProfile """
    client = Client()

    @tag('unit-test')
    def test_profile_access_url(self):
        """test_medicationList_access_url """
        response = self.client.get('users-profile')
        self.assertNotEqual(response.status_code, 300)

    @tag('unit-test')
    def test_profile_access_template(self):
        """test_medicationList_access_template """
        response = self.client.get('users-profile')
        self.assertNotEqual(response.status_code, 300)
        value = 'profile.html'
        self.assertTrue(value)
