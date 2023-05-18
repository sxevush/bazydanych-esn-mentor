from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, models


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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=20,
                                    choices=[('student', 'Student'), ('mentor', 'Mentor'), ('admin', 'Administrator')])

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_type']

    objects = CustomUserManager()


class FormAnswers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Questions(models.Model):
    question = models.CharField(max_length=255)


class Answer(models.Model):
    question = models.CharField(max_length=255)
    answer = models.IntegerField()
    form = models.ForeignKey(FormAnswers, on_delete=models.CASCADE)



