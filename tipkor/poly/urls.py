from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from .views import CardView, ConfirmView, LeafletView, SuccessView, BookletView

app_name = 'poly'

urlpatterns = [
    path('card/', CardView.as_view(), name='card'),
    path('leaflet/', LeafletView.as_view(), name='leaflet'),
    path('booklet/', BookletView.as_view(), name='booklet'),
    path('card/confirm/<pk>/', ConfirmView.as_view(), name='confirm'),
    path('leaflet/confirm/<pk>/', ConfirmView.as_view(), name='confirm'),
    path('booklet/confirm/<pk>/', ConfirmView.as_view(), name='confirm'),
    path('success/<pk>/', SuccessView.as_view(), name='success'),
]
