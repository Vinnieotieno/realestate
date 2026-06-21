from django.conf import settings
from services.models import Service
from legal.models import SEOSettings

SITE_NAME = getattr(settings, 'SITE_NAME', 'Kenya Realestate Platform')
SITE_TAGLINE = getattr(settings, 'SITE_TAGLINE', 'Premium Real Estate in Kenya')
SITE_DESCRIPTION = getattr(settings, 'SITE_DESCRIPTION', "Kenya's premier real estate platform")
SITE_KEYWORDS = getattr(settings, 'SITE_KEYWORDS', 'real estate Kenya, property Kenya')
SITE_URL = getattr(settings, 'SITE_URL', '').rstrip('/')


def global_context(request):
    """Add global context variables"""
    try:
        seo_settings = SEOSettings.objects.first()
    except Exception:
        seo_settings = None

    site_name = seo_settings.site_name if seo_settings and seo_settings.site_name else SITE_NAME
    site_description = seo_settings.site_description if seo_settings and seo_settings.site_description else SITE_DESCRIPTION
    site_keywords = seo_settings.site_keywords if seo_settings and seo_settings.site_keywords else SITE_KEYWORDS

    canonical_path = request.path
    if canonical_path != '/' and canonical_path.endswith('/'):
        canonical_path = canonical_path.rstrip('/')

    return {
        'featured_services': Service.objects.filter(is_featured=True, is_active=True).order_by('order')[:5],
        'seo_settings': seo_settings,
        'site_name': site_name,
        'site_tagline': SITE_TAGLINE,
        'site_description': site_description,
        'site_keywords': site_keywords,
        'site_url': SITE_URL or request.build_absolute_uri('/').rstrip('/'),
        'canonical_url': (SITE_URL or request.build_absolute_uri('/').rstrip('/')) + canonical_path,
    }
