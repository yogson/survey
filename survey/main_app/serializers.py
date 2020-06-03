from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *


BLANK_ERROR = {
    'answer_options': 'This field may not be blank.'
}

STARTED_ON_ERROR = {
    'started_on': 'This field is read-only.'
}

WRONG_DATA_ERROR = {
    'error': 'Inconsistent data.'
}


class SurveySerializer(serializers.ModelSerializer):
    # Serializer with additional update validation. We check for started_on.

    def update(self, instance, validated_data):
        if instance.started_on != self.initial_data.get('started_on'):
            raise ValidationError(detail=STARTED_ON_ERROR)

        return super().update(instance, validated_data)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'started_on', 'finished_on', 'questions']


class QuestionSerializer(serializers.ModelSerializer):
    # Serializer with additional validation. We check for options presence.

    def create(self, validated_data):
        new_question = self.initial_data
        if new_question.get('type') != Question.TYPE_CHOICES[0][0]:
            if not new_question.get('answer_options'):
                raise ValidationError(detail=BLANK_ERROR)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.type != Question.TYPE_CHOICES[0][0] and not self.initial_data.get('answer_options'):
            raise ValidationError(detail=BLANK_ERROR)

        return super().update(instance, validated_data)

    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'answer_options']


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerOption
        fields = ['id', 'option']


class AnswerSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        new_answer = self.initial_data
        question = Question.objects.get(pk=new_answer.get('question'))
        survey = Survey.objects.filter(
            started_on__lte=timezone.now()).filter(
            finished_on__gt=timezone.now()).filter(
            pk=new_answer.get('survey')
        )
        if survey and question:
            if question.type == question.TYPE_CHOICES[0][0]:
                if not new_answer.get('text') or new_answer.get('selected'):
                    raise ValidationError(detail=WRONG_DATA_ERROR)
            else:
                if not new_answer.get('selected') or new_answer.get('text'):
                    raise ValidationError(detail=WRONG_DATA_ERROR)

            return super().create(validated_data)

        else:
            raise ValidationError(detail=WRONG_DATA_ERROR)


    class Meta:
        model = Answer
        fields = ['id', 'user_id', 'survey', 'question', 'text', 'selected']
