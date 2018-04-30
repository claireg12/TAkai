from django import forms
from django.forms import ModelForm
from django.forms import BaseFormSet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from takai.models import *
from django.forms import BaseModelFormSet
import pdb


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text='Your password cannot be too similar to your other personal information, and cannot be a commonly used password. Your password must contain at least 8 characters and cannot be entirely numeric.' 

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
        exclude = ('theclass', 'semester', 'year')

class UpdateMSInfo(forms.ModelForm):
    class Meta:
        model = Mentorsessions
        fields = ['time', 'day','location']

class AddMSInfo(forms.ModelForm):
    class Meta:
        model = Mentorsessions
        fields = ['time', 'day','location']

class UpdateTaInfo(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(UpdateTaInfo, self).__init__(*args, **kwargs)

    #     # add custom error messages
    #     self.fields['student'].error_messages['unique'] = 'You do not have permission to edit this TA.'


    class Meta:
        model = Ta
        fields = ['student', 'bio']
        exclude = ('student',)

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class ClassesForm(ModelForm):
    class Meta:
        model = Classes
        fields = ['cid', 'name']

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['school', 'major', 'qualities', 'num_hours_week']
        labels = {
            'qualities': ('What qualities do you have that make you a good student mentor?'),
            'num_hours_week': ('Maximum number of hours available per week:'),
        }

class BaseArticleFormSet(BaseFormSet):
    def clean(self):
        """Checks that no two articles have the same title."""
        # pdb.set_trace()
        # super().clean()
        # self.fields['student'] = self.initial
        # pdb.set_trace()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        sessions = []
        # pdb.set_trace()
        for form in self.forms:
            # form.empty_permitted = False
            if not form.cleaned_data:
                form.add_error('interestcode', 'Did not complete form')
            else:
                session = form.cleaned_data['session']
                # pdb.set_trace()
                if session in sessions:
                    form.add_error('interestcode', 'Chose same class twice')
                    # raise forms.ValidationError("Please select your level of interest for every class listed exactly once")
                sessions.append(session)


class AvailabilityForm(ModelForm):
    AVAILABILITY_CHOICES  = (
        ('1','W 1:15-2:30pm'),
        ('2','W 2:45-4:00pm' ),
        ('3','Th 1:15-2:30pm' ),
        ('4','Th 2:45-4:00pm' ),
        ('5','F 1:15-2:30pm' ),
        ('6','F 2:45-4:00pm'))

    availabilitycode= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices = AVAILABILITY_CHOICES, label= '')
    class Meta:
        model = Availability
        fields = ['availabilitycode','student']
        exclude = ['student']

class ClassInterestForm(ModelForm):

    # def __init__(self, *args, student, **kwargs):
    #     self.student = student
    #     super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(ClassInterestForm, self).__init__(*args, **kwargs)
        # pdb.set_trace()
        # self.fields['student'] = self.initial

    class Meta:
        model = Classinterest
        fields = ['session', 'interestcode']

        labels = {
            'interestcode': ('Interest Level:'),
            'session':('Class'),
        }
    
