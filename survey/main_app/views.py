from django.utils import timezone
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .models import *
from .serializers import *


# TODO Change to FALSE!
class SurveyViewSet(viewsets.ModelViewSet):

    queryset = Survey.objects.filter(started_on__lte=timezone.now()).filter(finished_on__gt=timezone.now())
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Survey.objects.all()
        else:
            return self.queryset


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OptionViewSet(viewsets.ModelViewSet):

    queryset = AnswerOption.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RunViewSet(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        raise ValidationError(detail='Results are read-only')

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]


class ResultViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self, key=None):
        return self.queryset.filter(user_id=key)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(key=kwargs.get('pk')))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Answer.objects.all()
    serializer_class = DeepAnswerSerialier

