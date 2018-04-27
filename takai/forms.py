from django import forms
from django.forms import ModelForm
from django.contrib.messages.views import SuccessMessageMixin
from takai.models import *

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

    def __init__(self, *args, **kwargs):
        super(UpdateTaInfo, self).__init__(*args, **kwargs)

        # add custom error messages
        self.fields['student'].error_messages['unique'] = 'You do not have permission to edit this TA.'

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

class ClassInterestForm(ModelForm):
    class Meta:
        model = Classinterest
        fields = ['student', 'session', 'interestcode']
