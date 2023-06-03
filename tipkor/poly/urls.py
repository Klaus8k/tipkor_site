from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from .views import PolyView

urlpatterns = [
    path('card/', PolyView.as_view()),
]
