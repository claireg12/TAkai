from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from takai.models import *

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # self.fields['first'] = forms.IntegerField(max_value=max_values['first'])
        # add custom error messages
        # self.fields['graduation_year'].error_messages['unique'] = 'Please enter a valid graduation year.'
        # self.fields['id_number'].error_messages['unique'] = 'Please enter a valid ID number.'
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    id_number = forms.IntegerField(min_value=10000000, max_value=99999999, help_text='Please Enter your 8 digit student ID number.',
        error_messages={'min_value':'Please enter a valid ID number'})
    graduation_year = forms.IntegerField(min_value=2018)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id_number', 'graduation_year', 'password1', 'password2', )

class UpdateProfessorInfo(forms.ModelForm):
    class Meta:
        model = Professors
        fields = ['name', 'email', 'office', 'officehours']

class UpdateSessionInfo(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['theclass','semester','year','classroom','times']
        exclude = ('theclass',)
        labels = {
            'theclass': ('Class'),
        }

class UpdateMSInfo(forms.ModelForm):
    class Meta:
        model = Mentorsessions
        fields = ['time', 'day','location']

class AddMSInfo(forms.ModelForm):
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
        fields = ['semester', 'year', 'school', 'major', 'qualities', 'num_hours_week', 'lab_availability']

class ClassInterestForm(ModelForm):
    class Meta:
        model = Classinterest
        fields = ['student', 'session', 'interestcode']
        labels = {
            'interestcode': ('Interest Level:'),
            'session':('Class'),
        }
