from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['', 'poly', 'stamp', 'wide']

    def location(self, item):
        return f'/{item}'