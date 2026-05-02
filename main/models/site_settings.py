from django.db import models

class PlatformSettings(models.Model):
    logo = models.ImageField(upload_to='site_settings/logo/')
    favicon = models.ImageField(upload_to='site_settings/favicon/')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)

    # Contact and socials
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    email = models.EmailField()
    facebook = models.URLField()
    twitter = models.URLField()
    instagram = models.URLField()
    linkedin = models.URLField()
    youtube = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Platform Settings'
        verbose_name_plural = 'Platform Settings'

class NavLinks(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class FooterLinks(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    name = models.CharField(max_length=255)
    primary_color = models.CharField(max_length=100)
    secondary_color = models.CharField(max_length=100)
    bg_color = models.CharField(max_length=100)