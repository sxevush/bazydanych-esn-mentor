import numpy as np
from django.contrib.auth import login, logout
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import RegistrationForm, LoginForm, ProfileForm, FormAnswersForm, MentorSelectionForm
from .models import FormAnswer, Answer, MentoringChoice


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


def export_data():
    # wykonaj zapytanie SQL, aby pobrać wyniki z bazy danych
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT user_id, question1, question2, question3 FROM FormResult")
        results = cursor.fetchall()

    print(results)

    # utwórz tablicę numpy z pobranych wyników
    result_array = np.array(results)

    # konwertuj tablicę numpy na format CSV
    csv_data = np.array2string(result_array, separator=',', prefix='', suffix='')

    # ustaw nagłówek HTTP, aby przeglądarka pobierała plik CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wyniki.csv"'

    # zapisz dane CSV w odpowiedzi HTTP
    response.write(csv_data)

    # zwróć odpowiedź HTTP
    return response


def form_view(request):
    try:
        form_result = FormAnswer.objects.get(user=request.user)
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


def mentor_selection_view(request):
    if request.user.is_authenticated and request.user.account_type == 'student':
        try:
            MentoringChoice.objects.get(student=request.user, status='accepted')
            # TODO
            #  view do pokazywania mentora
            return redirect('panel')
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


def success(request):
    return render(request, 'success.html')


def already_filled(request):
    return render(request, 'already_filled.html')
