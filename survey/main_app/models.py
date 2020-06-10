from django.db import models
from datetime import datetime


class AnswerOption(models.Model):

    option = models.CharField(
        verbose_name='Option',
        max_length=512
    )

    def __str__(self):
        return self.option


class Question(models.Model):

    TYPE_CHOICES = [
        ('text', 'text'),
        ('one', 'one option'),
        ('multi', 'several options')
    ]

    title = models.CharField(
        verbose_name='Question',
        max_length=512
    )

    type = models.CharField(
        max_length=48,
        verbose_name='Question type',
        choices=TYPE_CHOICES
    )

    answer_options = models.ManyToManyField(
        AnswerOption,
        verbose_name='Options',
        blank=True
    )

    def __str__(self):
        return self.title


class Survey(models.Model):

    title = models.CharField(
        verbose_name='Survey title',
        max_length=512
    )

    started_on = models.DateField(
        verbose_name='Started date'
    )

    finished_on = models.DateField(
        verbose_name='Finished date'
    )

    description = models.TextField(
        max_length=1024,
        verbose_name='Description'
    )

    questions = models.ManyToManyField(
        Question,
        verbose_name='Questions',
        related_name='surveys',
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persisted_started_on = self.started_on if self.started_on else None

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.persisted_started_on:
            self.started_on = self.persisted_started_on
        super().save()
        self.persisted_started_on = self.started_on

    def start(self):
        self.started_on = datetime.now()


class Answer(models.Model):

    user_id = models.IntegerField(
        verbose_name='User ID'
    )

    survey = models.ForeignKey(
        Survey,
        verbose_name='Survey',
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        verbose_name='Question',
        related_name='answers',
        on_delete=models.CASCADE
    )

    selected = models.ManyToManyField(
        AnswerOption,
        verbose_name='Selected option(s)',
        blank=True
    )

    text = models.TextField(
        verbose_name='Text answer',
        max_length=1024,
        null=True, blank=True
    )



