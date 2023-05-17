from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djongo import models
from django import forms


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email jest wymagany.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)

    class Meta:
        abstract = True


class Questionnaire(models.Model):
    QUESTION_1 = 'Czy jesteś studentem AGH?'
    QUESTION_2 = 'Czy lubisz podróżować?'
    answers = models.JSONField()

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    _id = models.ObjectIdField
    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=20,
                                    choices=[('student', 'Student'), ('mentor', 'Mentor'), ('admin', 'Administrator')])
    profile = models.EmbeddedField(
        model_container=Profile,
        null=True
    )
    questionnaire = models.EmbeddedField(
        model_container=Questionnaire,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_type']

    objects = CustomUserManager()


# class FormResult(models.Model):  # odpowiedzi na pytania zostana zapisane w ten sposob do bazy danych
#     user_id = models.IntegerField()
#     question1 = models.IntegerField()
#     question2 = models.IntegerField()
#     question3 = models.IntegerField()
#     question4 = models.IntegerField()
#     question5 = models.IntegerField()
#     question6 = models.IntegerField()
#     question7 = models.IntegerField()
#     question8 = models.IntegerField()
#     question9 = models.IntegerField()
#     question10 = models.IntegerField()


class TenQuestionFormErasmo(models.Model):
    user_id = models.IntegerField()
    question1 = models.IntegerField(verbose_name="Na ile oceniasz swoje umiejętności komunikacyjne z ludźmi z innych kultur? (1 - bardzo słabo, 10 - bardzo dobrze)?")
    question2 = models.IntegerField(verbose_name="Jak bardzo ważne jest dla Ciebie, aby Twój mentor miał podobne zainteresowania naukowe jak Ty? (1 - nieważne, 10 - bardzo ważne)")
    question3 = models.IntegerField(verbose_name="Jak bardzo jesteś samodzielny w rozwiązywaniu problemów? (1 - potrzebuję dużo pomocy, 10 - radzę sobie sam)")
    question4 = models.IntegerField(verbose_name="Jak istotne jest dla Ciebie uczestniczenie w wydarzeniach kulturalnych i towarzyskich organizowanych przez uczelnię? (1 - mało istotne, 10 - bardzo istotne)")
    question5 = models.IntegerField(verbose_name="Na ile ważne jest dla Ciebie, aby Twój mentor był dostępny w sytuacjach awaryjnych? (1 - nieważne, 10 - bardzo ważne)")
    question6 = models.IntegerField(verbose_name="Jak oceniasz swoją znajomość języka polskiego? (1 - nie znam, 10 - płynnie)")
    question7 = models.IntegerField(verbose_name="Na ile chciałbyś/abyś aktywnie uczestniczyć w życiu studenckim AGH? (1 - niezbyt aktywnie, 10 - bardzo aktywnie)")
    question8 = models.IntegerField(verbose_name="Jak bardzo cenisz sobie wsparcie w codziennych sprawach, takich jak zakupy, korzystanie z komunikacji miejskiej czy uczelnianych usług? (1 - nieważne, 10 - bardzo ważne)")
    question9 = models.IntegerField(verbose_name="Na ile ważne jest dla Ciebie, aby Twój mentor miał doświadczenie w pracy z uczniami z Twojego kraju? (1 - nieważne, 10 - bardzo ważne)")
    question10 = models.IntegerField(verbose_name="Jak bardzo chciałbyś/abyś otrzymać wsparcie w kwestiach związanych z nauką, takich jak nauka przedmiotów, egzaminy czy projekty? (1 - nieważne, 10 - bardzo ważne)")
    created_at = models.DateTimeField(auto_now_add=True)


class TenQuestionFormMentor(models.Model):
    user_id = models.IntegerField()
    question1 = models.IntegerField(verbose_name="Na ile oceniasz swoje umiejętności komunikacyjne z ludźmi z innych kultur? (1 - bardzo słabo, 10 - bardzo dobrze)")
    question2 = models.IntegerField(verbose_name="Jak bardzo ważne jest dla Ciebie, aby student, którym się opiekujesz, miał podobne zainteresowania naukowe jak Ty? (1 - nieważne, 10 - bardzo ważne)")
    question3 = models.IntegerField(verbose_name="Jak bardzo jesteś skłonny pomagać studentowi w rozwiązywaniu problemów? (1 - chciałbym unikać, 10 - z przyjemnością pomogę)")
    question4 = models.IntegerField(verbose_name="Jak istotne jest dla Ciebie uczestniczenie w wydarzeniach kulturalnych i towarzyskich organizowanych przez uczelnię wraz ze studentem? (1 - mało istotne, 10 - bardzo istotne)")
    question5 = models.IntegerField(verbose_name="Na ile jesteś w stanie być dostępny dla studenta w sytuacjach awaryjnych? (1 - trudno mi będzie, 10 - zawsze gotów do pomocy)")
    question6 = models.IntegerField(verbose_name="Jak oceniasz swoją umiejętność komunikacji w języku angielskim lub innym języku obcym, którym posługuje się student? (1 - nie znam, 10 - płynnie)")
    question7 = models.IntegerField(verbose_name="Na ile chciałbyś/abyś aktywnie uczestniczyć w życiu studenckim AGH wraz ze studentem? (1 - niezbyt aktywnie, 10 - bardzo aktywnie)")
    question8 = models.IntegerField(verbose_name="Jak bardzo chciałbyś/abyś pomagać studentowi w codziennych sprawach, takich jak zakupy, korzystanie z komunikacji miejskiej czy uczelnianych usług? (1 - nieważne, 10 - bardzo ważne)")
    question9 = models.IntegerField(verbose_name="Jakie masz doświadczenie w pracy z uczniami z kraju, z którego pochodzi student? (1 - brak doświadczenia, 10 - dużo doświadczenia)")
    question10 = models.IntegerField(verbose_name="Jak bardzo chciałbyś/abyś wspierać studenta w kwestiach związanych z nauką, takich jak nauka przedmiotów, egzaminy czy projekty? (1 - nieważne, 10 - bardzo ważne)")
    created_at = models.DateTimeField(auto_now_add=True)
