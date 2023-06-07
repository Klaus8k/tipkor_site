from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from .views import BookletView, CardView, LeafletView

app_name = 'poly'

urlpatterns = [
    path('card/', CardView.as_view(), name='card'),
    path('leaflet/', LeafletView.as_view(), name='leaflet'),
    path('booklet/', BookletView.as_view()),
]
