import numpy as np
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm, ProfileForm, QuestionnaireForm, TenQuestionFormModelFormErasmo, \
    TenQuestionFormModelFormMentor
from .models import Profile, Questionnaire, TenQuestionFormErasmo, TenQuestionFormMentor


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

    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile()
        profile.save()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('panel')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


def fill_questionnaire(request):
    if not request.user.is_authenticated:
        return redirect('login')

    questionnaire_submitted = False
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = form.save(commit=False)
            user = request.user
            questionnaire.answers = {
                Questionnaire.QUESTION_1: form.cleaned_data.get('question_1'),
                Questionnaire.QUESTION_2: form.cleaned_data.get('question_2')
            }
            user.questionnaire = questionnaire
            # user.save(force_update=True)
            questionnaire.save()
            questionnaire_submitted = True
    else:
        form = QuestionnaireForm()
    return render(request, 'fill_questionnaire.html',
                  {'form': form, 'questionnaire_submitted': questionnaire_submitted})


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

    for results in (TenQuestionFormErasmo.objects.all(), TenQuestionFormModelFormMentor.objects.all()):
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


# def match_mentors():
#     students = Questionnaire.objects.filter(user__account_type='student')
#     mentors = Questionnaire.objects.filter(user__account_type='mentor')
#
#     matches = []
#
#     for student in students:
#         min_difference = float('inf')
#         best_mentor = None
#
#         for mentor in mentors:
#             total_difference = sum([abs(student.answers[key] - mentor.answers[key]) for key in student.answers])
#
#             if total_difference < min_difference:
#                 min_difference = total_difference
#                 best_mentor = mentor
#
#         matches.append((student, best_mentor))
#
#     return matches


@login_required
def edit_questionnaire(request):
    questionnaire, created = Questionnaire.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        questionnaire.answers = request.POST
        questionnaire.save()
        return redirect('home')
    return render(request, 'edit_questionnaire.html', {'questionnaire': questionnaire})


# def my_view(request):
#     form = MyForm()
#     if request.method == 'POST':
#         form = MyForm(request.POST)
#         if form.is_valid():
#             # zrób coś z danymi z formularza
#             pass
#     return render(request, 'my_template.html', {'form': form})


def form_view_erasmo(request):
    try:
        form_result = TenQuestionFormErasmo.objects.get(user_id=request.user.id)
        return redirect('already_filled')
    except TenQuestionFormErasmo.DoesNotExist:
        pass

    if request.method == 'POST':
        form = TenQuestionFormModelFormErasmo(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.user_id = request.user.id
            result.save()
            return redirect('success')
    else:
        form = TenQuestionFormModelFormErasmo()
    return render(request, 'form_erasmo.html', {'form': form})


# def form_view_mentor(request):
#     return render(request, 'form_mentor.html')

# def form_view_mentor(request):
#     if request.method == 'POST':
#         form = TenQuestionFormModelForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             result = FormResult(user_id=request.user.id, question1=data['question1'], question2=data['question2'],
#                                 question3=data['question3'], question4=data['question4'], question5=data['question5'],
#                                 question6=data['question6'], question7=data['question7'],
#                                 question8=data['question8'], question9=data['question9'], question10=data['question10'])
#             result.save()
#             return redirect('success')
#     else:
#         form = TenQuestionFormModelForm()
#     return render(request, 'form_mentor.html', {'form': form})
def form_view_mentor(request):
    try:
        form_result = TenQuestionFormMentor.objects.get(user_id=request.user.id)
        return redirect('already_filled')
    except TenQuestionFormMentor.DoesNotExist:
        pass

    if request.method == 'POST':
        form = TenQuestionFormModelFormMentor(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.user_id = request.user.id
            result.save()
            return redirect('success')
    else:
        form = TenQuestionFormModelFormMentor()
    return render(request, 'form_mentor.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def already_filled(request):
    return render(request, 'already_filled.html')

# wyswietlanie danych z bazy
# def ten_question_form_list(request):
#     client = MongoClient('localhost', 27017)
#     db = client['esn_mentor_db']
#     collection = db['ten_question_form']
#     forms = []
#     for form_data in collection.find():
#         form = TenQuestionForm(
#             user_id=form_data['user_id'],
#             question1=form_data['question1'],
#             question2=form_data['question2'],
#             question3=form_data['question3'],
#             question4=form_data['question4'],
#             question5=form_data['question5'],
#             question6=form_data['question6'],
#             question7=form_data['question7'],
#             question8=form_data['question8'],
#             question9=form_data['question9'],
#             question10=form_data['question10'],
#             created_at=form_data['created_at'],
#         )
#         forms.append(form)
#     return render(request, 'ten_question_forms.html', {'forms': forms})
