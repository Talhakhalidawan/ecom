from django.db import models

class StaticPage(models.Model):
    """
    Model for dynamic static pages like About Us, FAQ, Privacy Policy, etc.
    """
    title = models.CharField(max_length=200, help_text="The title of the page (e.g., 'About Us')")
    slug = models.SlugField(max_length=200, unique=True, help_text="The URL slug (e.g., 'about-us')")
    content = models.TextField(help_text="The main content of the page. Supports HTML.")
    
    # Metadata for SEO
    meta_description = models.CharField(max_length=255, blank=True, help_text="Description for search engines.")
    
    # Status & Dates
    is_active = models.BooleanField(default=True, help_text="Toggle to show/hide the page.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Static Page"
        verbose_name_plural = "Static Pages"
        ordering = ['title']

    def __str__(self):
        return self.title
