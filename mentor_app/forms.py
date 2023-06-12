from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.safestring import mark_safe

from .models import User, FormAnswer, Question, Answer, MentoringChoice


class RegistrationForm(UserCreationForm):
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
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            question_list = [question_obj.question for question_obj in
                             Question.objects.filter(user_group=user.account_type)]
        else:
            question_list = []
        for question in question_list:
            self.fields[question] = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(1, 11)]))

    def save(self, user):
        result = FormAnswer()
        result.user = user
        result.save()

        for (key, value) in self.cleaned_data.items():
            answer = Answer()
            answer.question = key
            answer.answer = value
            answer.form = result
            answer.save()



class MentorSelectionForm(forms.Form):
    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        users = User.objects.exclude(mentorships_left=0)
        request_sent = MentoringChoice.objects.filter(student=current_user)
        users = [user for user in users if user not in request_sent]
        user_choices = ((user.id, mark_safe(self.label_from_instance(user))) for user in users)

        self.fields['user_choices'] = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=user_choices
        )

    def save(self, current_user):
        result = MentoringChoice()
        result.student = current_user
        result.mentor = User.objects.get(pk=self.cleaned_data.get('user_choices'))
        result.status = 'pending'
        result.save()

    def label_from_instance(self, user):
        profile_url = f'/profile/{user.id}'
        return f'{user.first_name} {user.last_name}, {user.email} - <a href="{profile_url}">visit profile</a>'
