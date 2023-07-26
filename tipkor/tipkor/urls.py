from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('',TemplateView.as_view(template_name='tipkor.html')),
    path('wide/', include('wide.urls')),
    path('poly/', include('poly.urls')),
    
    path('expirement/', TemplateView.as_view(template_name='expirement.html')),
]
