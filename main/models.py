from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    ]
    
    CONCENTRATION_CHOICES = [
        ('mist', 'Body Mist / Splash'),
        ('edc', 'Eau de Cologne (EDC)'),
        ('edt', 'Eau de Toilette (EDT)'),
        ('edp', 'Eau de Parfum (EDP)'),
        ('parfum', 'Extrait de Parfum'),
        ('oil', 'Perfume Oil / Attar'),
    ]

    # Comprehensive Perfume Sizes
    SIZE_CHOICES = [
        (5, '5ml (Sample)'),
        (10, '10ml (Travel Size)'),
        (15, '15ml'),
        (30, '30ml'),
        (50, '50ml'),
        (75, '75ml'),
        (90, '90ml'),
        (100, '100ml'),
        (125, '125ml'),
        (150, '150ml'),
        (200, '200ml'),
        (250, '250ml'),
    ]
    
    # Core Details
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    
    # Perfume DNA
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    concentration = models.CharField(max_length=15, choices=CONCENTRATION_CHOICES, default='edp')
    size_ml = models.PositiveIntegerField(choices=SIZE_CHOICES, default=100)
    
    # Scent Profile
    top_notes = models.CharField(max_length=255, blank=True)
    heart_notes = models.CharField(max_length=255, blank=True)
    base_notes = models.CharField(max_length=255, blank=True)
    
    # Pricing & Inventory
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    
    # Marketing Flags
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name} {self.get_size_ml_display()}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.get_size_ml_display()}"
    
    @property
    def current_price(self):
        return self.sale_price if self.sale_price else self.base_price
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity <= self.low_stock_threshold

class ProductMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video (MP4/WebM)'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    file = models.FileField(upload_to='products/media/')
    
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name_plural = 'Product Media'
    
    def save(self, *args, **kwargs):
        if self.is_main:
            ProductMedia.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255, blank=True)
    comment = models.TextField()
    
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']