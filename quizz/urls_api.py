from django.conf.urls import url, include
import api
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'admin/operation/quizz/question/category', api.QuestionCategoryViewSet)
router.register(r'admin/operation/quizz/question', api.QuestionViewSet)
router.register(r'admin/operation/quizz/answer', api.AnswerViewSet)
router.register(r'admin/operation/quizz/quizz', api.QuizzViewSet)



urlpatterns = [
    url(r'^admin/operation/quizz/question/category/list/$', api.delete_list_category, name='delete-list-category'),
    url(r'^admin/operation/quizz/question/list/$', api.delete_list_question, name='delete-list-question'),
    url(r'^admin/operation/quizz/quizz/list/$', api.delete_list_quizz, name='delete-list-quizz'),
    url(r'^admin/operation/quizz/quizz/list/(?P<id>[0-9]+)/$', api.change_question_in_quizz, name='quizz-list'),
    url(r'^', include(router.urls)),

]
    