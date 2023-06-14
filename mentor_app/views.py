from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import RegistrationForm, LoginForm, ProfileForm, FormAnswersForm, MentorSelectionForm, MentorshipsLeftForm, \
    NewQuestionForm, AcceptStudentsForm
from .models import FormAnswer, User, MentoringChoice, Answer


def home(request):
    return render(request, 'home.html')


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('panel')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_protect
def log_in(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('panel')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('login')


def panel(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'panel.html')


@csrf_protect
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('panel')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


def profile_view(request, id):
    user = User.objects.get(pk=id)
    try:
        form = FormAnswer.objects.get(user=user)
        answers = Answer.objects.filter(form=form)
    except FormAnswer.DoesNotExist:
        answers = None
    return render(request, 'profile.html', {'user': user, 'answers': answers})


def form_view(request):
    try:
        form = FormAnswer.objects.get(user=request.user)
        return redirect('already_filled')
    except FormAnswer.DoesNotExist:
        pass

    if request.method == 'POST':
        form = FormAnswersForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('success')
    else:
        form = FormAnswersForm(user=request.user)  # Pass user to the form
    return render(request, 'form.html', {'form': form})


def add_question_view(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel')
    else:
        form = NewQuestionForm()

    return render(request, 'add_question.html', {'form': form})


def mentor_selection_view(request):
    if request.user.is_authenticated and request.user.account_type == 'student':
        try:
            mentor = MentoringChoice.objects.get(student=request.user, status='accepted').mentor
            return redirect('profile', mentor.id)
        except MentoringChoice.DoesNotExist:
            pass

        if request.method == 'POST':
            form = MentorSelectionForm(request.POST, current_user=request.user)
            if form.is_valid():
                form.save(request.user)
                return redirect('success')
        else:
            form = MentorSelectionForm(current_user=request.user)
        return render(request, 'mentor_select.html', {'form': form})
    else:
        return redirect('panel')


def accept_students_view(request):
    if request.user.is_authenticated and request.user.account_type == 'mentor':
        if request.method == 'POST':
            form = AcceptStudentsForm(request.POST, user=request.user)
            if form.is_valid():
                form.save(request.user)
                return redirect('success')
        else:
            form = AcceptStudentsForm(user=request.user)
        return render(request, 'accept_students.html', {'form': form})
    else:
        return redirect('panel')


def edit_mentorships(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.account_type == 'mentor':
        if request.method == 'POST':
            form = MentorshipsLeftForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('panel')
        else:
            form = MentorshipsLeftForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form': form})
    else:
        return redirect('panel')


def success(request):
    return render(request, 'success.html')


def already_filled(request):
    return render(request, 'already_filled.html')
