from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from .views import BannerView, StickerView, TableView, ConfirmView, SuccessView

app_name = 'wide'

urlpatterns = [
    path('banner/', BannerView.as_view(), name='banner'),
    path('sticker/', StickerView.as_view(), name='sticker'),
    path('table/', TableView.as_view(), name='table'),
    path('banner/confirm/<pk>/', ConfirmView.as_view(), name='confirm'),
    path('sticker/confirm/<pk>/', ConfirmView.as_view(), name='confirm'),
    path('table/confirm/<pk>/', ConfirmView.as_view(), name='confirm'),
    path('success/<pk>/', SuccessView.as_view(), name='success'),
]