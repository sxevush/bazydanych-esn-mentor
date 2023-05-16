from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import models

from .models import User, Profile, Questionnaire


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'account_type', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username')


# class QuestionnaireForm(forms.ModelForm):
#     question = forms.CharField(max_length=200, label='Question')
#
#     class Meta:
#         model = Questionnaire
#         fields = ('answers', 'question',)

class QuestionnaireForm(forms.ModelForm):
    question_1 = forms.ChoiceField(choices=[('tak', 'Tak'), ('nie', 'Nie')], label='Czy jesteś studentem AGH?',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    question_2 = forms.ChoiceField(choices=[('tak', 'Tak'), ('nie', 'Nie')], label='Czy lubisz podróżować?',
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Questionnaire
        fields = ('answers', 'question_1', 'question_2',)


# class MyForm(forms.Form):
#     my_field = forms.CharField(max_length=100)


from django import forms
from .models import TenQuestionFormErasmo, TenQuestionFormMentor


class TenQuestionFormModelFormMentor(forms.ModelForm):
    class Meta:
        model = TenQuestionFormMentor
        fields = (
            'question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7', 'question8',
            'question9', 'question10')
        widgets = {
            'question1': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question2': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question3': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question4': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question5': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question6': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question7': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question8': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question9': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question10': forms.Select(choices=[(i, i) for i in range(1, 11)])
        }

class TenQuestionFormModelFormErasmo(forms.ModelForm):
    class Meta:
        model = TenQuestionFormErasmo
        fields = (
            'question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7', 'question8',
            'question9', 'question10')
        widgets = {
            'question1': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question2': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question3': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question4': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question5': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question6': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question7': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question8': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question9': forms.Select(choices=[(i, i) for i in range(1, 11)]),
            'question10': forms.Select(choices=[(i, i) for i in range(1, 11)])
        }



    # class Meta:
    #     model = TenQuestionForm
    #     fields = ['question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7',
    #               'question8', 'question9', 'question10']
