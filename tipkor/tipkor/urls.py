from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from .views import PolyView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name='old_index.html')),
    path('', PolyView.as_view(template_name='old_index.html')),
]
