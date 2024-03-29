from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('',TemplateView.as_view(template_name='tipkor.html'), name='tipkor'),
    path('wide/', include('wide.urls'), name='wide'),
    path('poly/', include('poly.urls'), name='poly'),
    path('stamp/', include('stamp.urls'), name='stamp'),
    path('politica/', TemplateView.as_view(template_name='politica.html'), name='politica'),
    path('sitemap.xml',TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    path('robots.txt',TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    path('expirement/', TemplateView.as_view(template_name='expirement.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = 'tipkor.views.error_404_view'
handler500 = 'tipkor.views.server_error'
