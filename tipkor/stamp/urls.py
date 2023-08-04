from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from .views import ConfirmView, CstampView, RstampView, SuccessView

app_name = 'stamp'

urlpatterns = [
    path('c_stamp/', CstampView.as_view(), name='c_stamp'),
    path('c_stamp/confirm/', ConfirmView.as_view(), name='confirm'),
    path('c_stamp/<pk>/', CstampView.as_view(), name='c_stamp'),
    
    path('r_stamp/', RstampView.as_view(), name='r_stamp'),
    path('r_stamp/confirm/', ConfirmView.as_view(), name='confirm'),
    path('r_stamp/<pk>/', RstampView.as_view(), name='r_stamp'),
    
    path('success/<pk>/', SuccessView.as_view(), name='success'),
]
