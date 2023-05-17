from django.contrib import admin
from .models import User, TenQuestionFormMentor, TenQuestionFormErasmo

admin.site.register(User)


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
    search_fields = ('user_id', 'question1')
    ordering = ('user_id',)


admin.site.register(TenQuestionFormErasmo, ContactAdminErasmo)



