from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from legal.views import sitemap_xml, robots_txt

urlpatterns = [
    path('', include('pages.urls')),
    path('listings/', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('contacts/', include('contacts.urls')),
    path('blog/', include('blog.urls')),
    path('services/', include('services.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('property-management/', include('property_management.urls')),
    path('api/property-management/', include('property_management.api_urls')),
    path('legal/', include('legal.urls')),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
