from .models import PlatformSettings, NavLinks, FooterLinks, SiteSettings

def site_context(request):
    """
    Global context processor for site-wide settings and links.
    """
    settings = PlatformSettings.objects.first()
    nav_links = NavLinks.objects.filter(is_active=True)
    footer_links = FooterLinks.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.all().first()
    
    return {
        'platform_settings': settings,
        'nav_links': nav_links,
        'footer_links': footer_links,
        'site_settings': site_settings,
    }
