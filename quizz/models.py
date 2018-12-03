# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from main.models import DateTimeAuthModel, DateTimeModel

# Create your models here.


@python_2_unicode_compatible
class QuestionCategory(DateTimeModel):
    name = models.CharField(_('Name'), max_length=255)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='childrens', on_delete=models.SET_NULL)
    description = models.CharField(
        _('Decription'), max_length=255, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Question Category')


@python_2_unicode_compatible
class Question(DateTimeAuthModel):
    name = models.CharField(_('Name'), max_length=255)
    content = models.TextField(_('Content'))
    category = models.ForeignKey(QuestionCategory, related_name='question_category_rel',
                                 on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.content)

    class Meta:
        verbose_name = _('Question')


@python_2_unicode_compatible
class Answer(DateTimeAuthModel):
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(_('Content'))
    is_correct = models.BooleanField(_('Is correct'), default=False)

    def __str__(self):
        return "%s" % (self.question)

    class Meta:
        verbose_name = _('Answer')


@python_2_unicode_compatible
class Quizz(DateTimeAuthModel):
    name = models.CharField(_('Name'), max_length=255)
    description = models.CharField(
        _('Decription'), max_length=255, null=True, blank=True)
    questions = models.ManyToManyField(
        Question, through='QuizzQuestion', blank=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Quizz')


@python_2_unicode_compatible
class QuizzQuestion(DateTimeModel):
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.quizz)

    class Meta:
        verbose_name = _('Quizz Question')
        unique_together = ("quizz", "question")
