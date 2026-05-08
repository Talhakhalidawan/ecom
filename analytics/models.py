from django.db import models
from django.conf import settings
from products.models import Product

class PageVisit(models.Model):
    path = models.CharField(max_length=255)
    referrer = models.URLField(max_length=500, blank=True, null=True)
    session_key = models.CharField(max_length=40, db_index=True, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Page Visits"

    def __str__(self):
        return f"{self.path} at {self.created_at}"

class ProductEvent(models.Model):
    EVENT_TYPES = [
        ('click', 'Click'),
        ('view', 'View'),
        ('add_to_cart', 'Add to Cart'),
        ('wishlist', 'Add to Wishlist'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='analytics_events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    session_key = models.CharField(max_length=40, db_index=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product Event"
        verbose_name_plural = "Product Events"

    def __str__(self):
        return f"{self.product.name} - {self.event_type}"
