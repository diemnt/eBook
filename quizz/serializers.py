from rest_framework import serializers
from quizz.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionCategory
        fields = ('id', 'name', 'parent', 'description')


class DisplayCategorySerializer(serializers.ModelSerializer):
    count_question = serializers.SerializerMethodField()

    class Meta:
        model = QuestionCategory
        fields = ('id', 'name', 'childrens', 'description', 'count_question', 'parent')

    # Count question when list all category
    def get_count_question(self, obj):
        return obj.question_category_rel.count()

    # Set serializer for nested childrens
    def get_fields(self):
        fields = super(DisplayCategorySerializer, self).get_fields()
        fields['childrens'] = DisplayCategorySerializer(many=True)
        return fields


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(
        many=False, queryset=QuestionCategory.objects.all())

    class Meta:
        model = Question
        fields = '__all__'

    # Create answer with question together
    def create(self, validated_data):
        if self.context['request'].user.is_authenticated():
            validated_data['created_by'] = self.context['request'].user.staff

        answer_data = validated_data.pop('answer_set')
        question = Question.objects.create(**validated_data)
        for answer in answer_data:
            Answer.objects.create(question=question, **answer)
        return question

    # Create or update answer with question together
    def update(self, instance, validated_data):
        if self.context['request'].user.is_authenticated():
            validated_data['modified_by'] = self.context['request'].user.staff

        answer_data = validated_data.pop('answer_set')
        for answer in answer_data:
            if answer.get('id'):
                answer = Answer.objects.filter(
                    id=answer['id']).update(**answer)
            else:
                answer = Answer.objects.create(question=instance, **answer)

        return super(QuestionSerializer, self).update(instance, validated_data)

# Display list question
class DisplayQuestionSerializer(serializers.ModelSerializer):
    in_quizz = serializers.SerializerMethodField()
    created_by = serializers.CharField(source = 'created_by.user.username', default=None)
    modified_by = serializers.CharField(source = 'modified_by.user.username', default=None)

    class Meta:
        model = Question
        fields = '__all__'

    # Check question is in quizz
    def get_in_quizz(self, obj):
        is_in_quizz = obj.quizz_set.count()
        return True if is_in_quizz else False


class QuizzSerializer(serializers.ModelSerializer):
    in_book = serializers.SerializerMethodField()
    questions = DisplayQuestionSerializer(many=True, read_only = True)

    class Meta:
        model = Quizz
        fields = '__all__'

    def get_in_book(self, obj):
        is_in_book = obj.book_set.count()
        return True if is_in_book else False


class QuizzQuestionSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all())

    class Meta:
        model = QuizzQuestion
        fields = '__all__'

    # Validate question is in quizz
    def validate(self, data):
        exist_question = QuizzQuestion.objects.filter(quizz = data['quizz'], question__in = data['question'] )
        if exist_question:
            raise serializers.ValidationError(_("Question is exist in quizz."))
        return data
    
    # Create QuizzQuestion with list question
    def create(self, validated_data):
        list_question = validated_data['question']
        quizz = validated_data['quizz']
        quizz_question = [QuizzQuestion(quizz=quizz, question=question) for question in list_question]
        QuizzQuestion.objects.bulk_create(quizz_question)
        return quizz_question



