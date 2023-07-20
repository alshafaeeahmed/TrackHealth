"""forms file """
from django import forms
from django.contrib.auth.models import User
from . import models


class NurseUserForm(forms.ModelForm):
    """NurseUserForm """
    class Meta:
        """Meta """
        def pub1(self):
            """pub1 """


        def pub2(self):
            """pub2 """

        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class NurseForm(forms.ModelForm):
    """NurseForm """
    class Meta:
        """Meta """
        def pub1(self):
            """pub1 """


        def pub2(self):
            """pub2 """

        model = models.Nurse
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']


class PatientUserForm(forms.ModelForm):
    """PatientUserForm """
    class Meta:
        """Meta """
        def pub1(self):
            """pub1 """


        def pub2(self):
            """pub2 """

        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class PatientForm(forms.ModelForm):
    """PatientForm """
    class Meta:
        """Meta """
        def pub1(self):
            """pub1 """


        def pub2(self):
            """pub2 """

        model = models.Patient
        fields = ['address', 'status', 'symptoms', 'profile_pic', 'gender', 'age']


class FeedbackForm(forms.ModelForm):
    """FeedbackForm """
    class Meta:
        """Meta """
        def pub1(self):
            """pub1 """

        def pub2(self):
            """pub2 """
        model = models.Feedback
        fields = ['by', 'message', 'senderType']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'cols': 30}),
        }


class MedicationForm(forms.ModelForm):
    """MedicationForm """
    class Meta:
        """Meta """
        def pub1(self):
            """pub1 """


        def pub2(self):
            """pub2 """

        model = models.Medication
        fields = ['name', 'numOftimes', 'mg', 'expiratDate', 'Description']


class ContactForm(forms.Form):
    """ContactForm """
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
