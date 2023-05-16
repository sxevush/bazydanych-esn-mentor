from django.contrib import admin
from .models import User, Profile, Question, Questionnaire

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Questionnaire)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User
#
# class CustomUserAdmin(UserAdmin):
#     list_display = ('email', 'account_type', 'first_name', 'last_name', 'is_active')
#     list_filter = ('account_type', 'is_active', 'is_staff', 'is_superuser')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#
# admin.site.register(User, CustomUserAdmin)
from django.contrib import admin
from .models import TenQuestionFormMentor, TenQuestionFormErasmo

class ContactAdminMentor(admin.ModelAdmin):
    list_display = ('user_id', 'question1', 'question2', 'question3', 'question4', 'question5',
                    'question6', 'question7', 'question8', 'question9', 'question10')
    list_filter = ('user_id',)
    search_fields = ('user_id',)
    ordering = ('user_id',)

admin.site.register(TenQuestionFormMentor, ContactAdminMentor)

class ContactAdminErasmo(admin.ModelAdmin):
    list_display = ('user_id', 'question1', 'question2', 'question3', 'question4', 'question5',
                    'question6', 'question7', 'question8', 'question9', 'question10')
    list_filter = ('user_id',)
    search_fields = ('user_id','question1')
    ordering = ('user_id',)

admin.site.register(TenQuestionFormErasmo, ContactAdminErasmo)



