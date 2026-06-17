from services.models import Service
from legal.models import SEOSettings

def global_context(request):
    """Add global context variables"""
    try:
        seo_settings = SEOSettings.objects.first()
    except SEOSettings.DoesNotExist:
        seo_settings = None
    
    return {
        'featured_services': Service.objects.filter(is_featured=True, is_active=True).order_by('order')[:5],
        'seo_settings': seo_settings,
    }
