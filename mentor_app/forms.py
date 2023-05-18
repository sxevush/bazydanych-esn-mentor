from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, FormAnswers, Questions, Answer


class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'account_type', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class FormAnswersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        question_list = [question_obj.question for question_obj in Questions.objects.all()]
        for question in question_list:
            self.fields[question] = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 11)]))

    def save(self, user):
        result = FormAnswers()
        result.user = user
        result.save()

        for (key, value) in self.cleaned_data.items():
            answer = Answer()
            answer.question = key
            answer.answer = value
            answer.form = result
            answer.save()

    class Meta:
    #     question_list = [question_obj.question for question_obj in Questions.objects.all()]
    #     print(question_list)
    #     question_widgets = {}
    #     for question in question_list:
    #         question_widgets[question] = forms.Select(choices=[(i, i) for i in range(1, 11)])
    #         question_widgets[question].render(question, question)
    #
        fields = []
        widgets = {}
