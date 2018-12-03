# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizz.models import *
# Register your models here.



class QuestionCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuestionCategory, QuestionCategoryAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'question')

admin.site.register(Answer, AnswerAdmin)

class AnswerInline(admin.TabularInline):
	model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = (
    	AnswerInline,
    )
admin.site.register(Question, QuestionAdmin)

class QuizzQuestionInline(admin.TabularInline):
    model = QuizzQuestion

class QuizzAdmin(admin.ModelAdmin):
    inlines = (
       QuizzQuestionInline,
    )
admin.site.register(Quizz, QuizzAdmin)

