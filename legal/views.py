from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from .models import LegalPage, Sitemap
from listings.models import Listing
from services.models import Service
from blog.models import Blog

def legal_page(request, slug):
    """Display legal page"""
    page = get_object_or_404(LegalPage, slug=slug, is_active=True)
    
    context = {
        'page': page,
        'last_updated': page.last_updated,
        'effective_date': page.effective_date,
    }
    return render(request, 'legal/legal_page.html', context)

def privacy_policy(request):
    """Privacy policy shortcut"""
    page = get_object_or_404(LegalPage, page_type='privacy', is_active=True)
    return legal_page(request, page.slug)

def terms_of_service(request):
    """Terms of service shortcut"""
    page = get_object_or_404(LegalPage, page_type='terms', is_active=True)
    return legal_page(request, page.slug)

def sitemap_xml(request):
    """Generate dynamic XML sitemap"""
    # Static pages
    static_urls = [
        {'url': '/', 'priority': 1.0, 'changefreq': 'daily'},
        {'url': '/about/', 'priority': 0.8, 'changefreq': 'monthly'},
        {'url': '/contact/', 'priority': 0.8, 'changefreq': 'monthly'},
        {'url': '/listings/', 'priority': 0.9, 'changefreq': 'daily'},
        {'url': '/services/', 'priority': 0.8, 'changefreq': 'weekly'},
    ]
    
    # Dynamic content
    listings = Listing.objects.public().values('slug', 'list_date')
    services = Service.objects.filter(is_active=True).values('slug', 'updated_at')
    blogs = Blog.objects.filter(published=True).values('slug', 'posted_at')
    legal_pages = LegalPage.objects.filter(is_active=True).values('slug', 'last_updated')
    
    # Custom sitemap entries
    custom_urls = Sitemap.objects.filter(is_active=True)
    
    context = {
        'static_urls': static_urls,
        'listings': listings,
        'services': services,
        'blogs': blogs,
        'legal_pages': legal_pages,
        'custom_urls': custom_urls,
        'domain': request.get_host(),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    
    xml_content = render_to_string('legal/sitemap.xml', context)
    return HttpResponse(xml_content, content_type='application/xml')

def robots_txt(request):
    """Generate robots.txt"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    
    return HttpResponse('\n'.join(lines), content_type='text/plain')