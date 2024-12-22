from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shirts.models import Shirt
from django.utils.timezone import now

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return ['home:index', 'shirts:shirt_list', 'account_login', 'account_signup']

    def location(self, item):
        return reverse(item)

class ShirtSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Shirt.objects.all().order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at if obj.updated_at else now()
