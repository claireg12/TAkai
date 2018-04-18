from django import forms
from django.forms import ModelForm
from takai.models import Professors,Session, Classes, Application

class UpdateProfessorInfo(forms.ModelForm):
     class Meta:
       model = Professors
       fields = ['name', 'email', 'office', 'officehours']


class UpdateSessionInfo(forms.ModelForm):
     class Meta:
        model = Session
        fields = ['theclass', 'semester', 'year','classroom','times']

class ClassesForm(ModelForm):
    class Meta:
        model = Classes
        fields = ['cid', 'name']

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['student', 'school', 'major', 'qualities', 'num_hours_week', 'lab_availability']
