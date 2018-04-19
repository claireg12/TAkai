from django import forms
from django.forms import ModelForm
<<<<<<< HEAD
from django.contrib.messages.views import SuccessMessageMixin
from takai.models import *
=======
from takai.models import Professors,Session, Classes, Application
>>>>>>> 801d6dcf3ad2adfc4f571aedfd07626abda0748e

class UpdateProfessorInfo(forms.ModelForm):
    class Meta:
        model = Professors
        fields = ['name', 'email', 'office', 'officehours']


class UpdateSessionInfo(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['theclass', 'semester', 'year','classroom','times']
        labels = {
            'theclass': ('Class'),
        }

class UpdateMSInfo(forms.ModelForm):
    class Meta:
        model = Mentorsessions
        fields = ['time', 'day','location']

class UpdateTaInfo(forms.ModelForm):
    class Meta:
        model = Ta
        fields = ['student', 'bio']
        error_messages = {
            'unique': 'You do not have permissions to edit other TAs or TA already exists',
        }

class ClassesForm(ModelForm):
    class Meta:
        model = Classes
        fields = ['cid', 'name']

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['student', 'school', 'major', 'qualities', 'num_hours_week', 'lab_availability']
