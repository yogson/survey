from django.contrib import admin
from .models import *


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('started_on',)


admin.site.register(AnswerOption)
admin.site.register(Question)
admin.site.register(Answer)
