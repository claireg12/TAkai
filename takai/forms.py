from django import forms
from django.forms import ModelForm
from takai.models import *

class UpdateProfessorInfo(forms.ModelForm):
    class Meta:
        model = Professors
        fields = ['name', 'email', 'office', 'officehours']


class UpdateSessionInfo(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['theclass', 'semester', 'year','classroom','times']

class UpdateHostInfo(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['student', 'mentorsesh']


class UpdateTaInfo(forms.ModelForm):
    class Meta:
        model = Ta
        fields = ['student', 'bio']