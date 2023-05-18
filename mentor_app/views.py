import numpy as np
from django.contrib.auth import login, logout
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ProfileForm, FormAnswersForm
from .models import FormAnswers, Answer


def home(request):
    return render(request, 'home.html')


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


# TODO poprawić edit_profile, żeby miało jakiś sens
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.username = form.cleaned_data['username']
            request.user.save()
            return redirect('panel')
    else:
        form = ProfileForm()

    return render(request, 'edit_profile.html', {'form': form})


def admin_panel(request):
    return render(request, 'admin_panel.html')


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


def show_results(request):
    # utwórz listę wyników
    result_list = []

    for results in (FormAnswers.objects.all()):
        for result in results:
            # dodaj wynik do listy jako krotkę
            result_tuple = (result.user_id, result.question1, result.question2, result.question3, result.question4,
                            result.question5, result.question6, result.question7, result.question8, result.question9,
                            result.question10)
            result_list.append(result_tuple)

    # utwórz tablicę NumPy z listy wyników
    result_array = np.array(result_list)

    # przekaż tablicę NumPy do szablonu HTML
    return render(request, 'admin_panel.html', {'results': result_array})


# def my_view(request):
#     form = MyForm()
#     if request.method == 'POST':
#         form = MyForm(request.POST)
#         if form.is_valid():
#             # zrób coś z danymi z formularza
#             pass
#     return render(request, 'my_template.html', {'form': form})


def form_view(request):
    try:
        form_result = FormAnswers.objects.get(user=request.user)
        return redirect('already_filled')
    except FormAnswers.DoesNotExist:
        pass

    if request.method == 'POST':
        form = FormAnswersForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('success')
    else:
        form = FormAnswersForm()
    return render(request, 'form.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def already_filled(request):
    return render(request, 'already_filled.html')
