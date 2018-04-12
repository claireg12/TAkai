from django import forms
from django.forms import ModelForm
from takai.models import Professors,Session

class UpdateProfessorInfo(forms.ModelForm):
     class Meta:
       model = Professors
       fields = ['name', 'email', 'office', 'officehours']


class UpdateSessionInfo(forms.ModelForm):
     class Meta:
        model = Session
        fields = ['theclass', 'semester', 'year','classroom','times']
