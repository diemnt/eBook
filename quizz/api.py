# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from quizz.models import *
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, mixins
from serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from staff.permission_class import RolePermission
from staff.decorators import check_role_permission
from rest_framework import status


'''
    ******  START STAFF MODULE  ********
'''


class QuestionCategoryViewSet(viewsets.ModelViewSet):

    queryset = QuestionCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (RolePermission, )

    def list(self, request):
        queryset = QuestionCategory.objects.filter(parent__isnull=True)
        serializer = DisplayCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete category don't has question
        category_has_question = instance.question_category_rel.count()
        if category_has_question:
            return Response({"code": 400, 'message': _('Không thể xóa danh mục.')}, status=400)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
    Funtion delete_list_category
    Delete list category
    Author: Hoang nguyen
'''


@api_view(['DELETE'])
@check_role_permission('questioncategory_delete')
def delete_list_category(request):
    try:
        list_category = request.data.get('list_category', None)
        if list_category:
            # Delete category which has no question
            category = QuestionCategory.objects.filter(id__in=list_category, question_category_rel__isnull=True)
            list_category_valid = category.values_list('id', flat = True)

            # If list_category is in list_category_valid then delete
            check_sub_set = set(list_category).issubset(set(list_category_valid))
            if check_sub_set:
                category.delete()
                return Response({'message': _('Thành công.')})
            return Response({"code": 400, 'message': _('Không thể xóa danh mục.')}, status=400)
        return Response({"code": 400, "message": _("Danh sách danh mục là bắt buộc.")}, status=400)
    except Exception, e:
        print 'delete_list_category ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống"), "fields": ""}, status=500)




class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (RolePermission, )
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category',)

    # Show name and content question when list

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = DisplayQuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Delete question is not in quizz
        question_in_quizz = instance.quizz_set.count()
        if question_in_quizz:
            return Response({"code": 400, 'message': _('Không thể xóa câu hỏi.')}, status=400)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerViewSet(mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (RolePermission, )


'''
    Funtion delete_list_question
    Delete list question
    Author: Hoang nguyen
'''


@api_view(['DELETE'])
@check_role_permission('question_delete')
def delete_list_question(request):
    try:
        list_question = request.data.get('list_question', None)
        if list_question:
            question = Question.objects.filter(
                id__in=list_question, quizz__isnull=True)
            list_question_valid = question.values_list('id', flat = True)
            
            # If list_question is in list_question_valid then delete
            check_sub_set = set(list_question).issubset(set(list_question_valid))
            if check_sub_set:
                question.delete()
                return Response({'message': _('Thành công.')})
            return Response({"code": 400, 'message': _('Không thể xóa câu hỏi.'), "fields": ""}, status=400)
        return Response({"code": 400, "message": _("Danh sách câu hỏi là bắt buộc."), "fields": ""}, status=400)
    except Exception, e:
        print 'delete_list_question ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống"), "fields": ""}, status=500)


class QuizzViewSet(viewsets.ModelViewSet):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
    permission_classes = (RolePermission, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Delete quizz don't use in book
        quizz_has_book = instance.book_set.count()
        if quizz_has_book:
            return Response({"code": 400, 'message': _('Không thể xóa đề thi.')}, status=400)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
    change_question_in_quizz
    Add and remove question in quiz
    Author: Hoang nguyen
'''


@api_view(['POST', 'DELETE'])
@check_role_permission('quizz_edit')
def change_question_in_quizz(request, id):
    try:
        list_question_id = request.data.get('list_question_id', None)
        if not list_question_id:
            return Response({"code": 400, 'message': _('Không tìm thấy danh sách câu hỏi.'), "fields": ""}, status=400)
        
        quizz = Quizz.objects.get(id=id)

        if request.method == 'POST':
            # Only create new question id
            serializer = QuizzQuestionSerializer(data = {'question': list_question_id, 'quizz': quizz.id})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Thành công.'})
            return Response({"code": 400, 'message': serializer.errors, "fields": ""}, status=400)
        else:
            # Delete question in quizz
            list_quizz_question = QuizzQuestion.objects.filter(quizz=quizz, question_id__in=list_question_id)
            list_question_id_valid = list_quizz_question.values_list('question_id', flat = True)
            
            # If list_question_id is in list_question_id_valid then delete
            check_sub_set = set(list_question_id).issubset(set(list_question_id_valid))
            if check_sub_set:
                list_quizz_question.delete()
                return Response({'message': 'Thành công.'})
            return Response({"code": 400, 'message': _('Không thể gỡ bỏ câu hỏi.'), "fields": ""}, status=400)

    except Quizz.DoesNotExist, e:
        return Response({"code": 400, "message": _("Không tìm thấy đề thi này"), "fields": ""}, status=400)
    except Exception, e:
        print 'QuizzList ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống"), "fields": ""}, status=500)



'''
    Funtion delete_list_quizz
    Delete list quizz
    Author: Hoang nguyen
'''


@api_view(['DELETE'])
@check_role_permission('quizz_delete')
def delete_list_quizz(request):
    try:
        list_quizz = request.data.get('list_quizz', None)
        # Delete list quizz has no book
        if list_quizz:
            quizz = Quizz.objects.filter(
                id__in=list_quizz, book__isnull=True)
            list_quizz_valid = quizz.values_list('id', flat = True)

            # If list_quizz is in list_quizz_valid then delete
            check_sub_set = set(list_quizz).issubset(set(list_quizz_valid))
            if check_sub_set:
                quizz.delete()
                return Response({'message': _('Thành công.')})
            return Response({"code": 400, 'message': _('Không thể xóa đề thi.'), "fields": ""}, status=400)
        return Response({"code": 400, "message": _("Danh sách đề thi là bắt buộc."), "fields": ""}, status=400)
    except Exception, e:
        print 'delete_list_question ', e
        return Response({"code": 500, "message": _("Lỗi hệ thống"), "fields": ""}, status=500)






'''
    ******  END STAFF MODULE  ********
'''







