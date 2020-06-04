from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from main_app.views import SurveyViewSet, QuestionViewSet, OptionViewSet, RunViewSet, ResultViewSet


router = routers.SimpleRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)
router.register(r'run', RunViewSet)
router.register(r'result', ResultViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
