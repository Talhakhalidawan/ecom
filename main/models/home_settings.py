from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class HeroSlide(models.Model):
    """
    Dynamic Hero Carousel items.
    """
    big_image = models.ImageField(upload_to='home/hero/')
    small_image = models.ImageField(upload_to='home/hero/', help_text="Mobile image")
    link = models.CharField(max_length=255)
    
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Hero Slide {self.display_order}"


class StoreFeature(models.Model):
    """
    Minimal features bar (e.g., Complimentary Shipping, Authenticity).
    """
    text = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.text


class ProductSection(models.Model):
    """
    Handles both product carousels and product grids.
    """
    DISPLAY_CHOICES = (
        ('carousel', 'Carousel'),
        ('grid', 'Grid'),
    )
    SIZE_CHOICES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    )
    WIDTH_CHOICES = (
        ('standard', 'Standard (1280px)'),
        ('wide', 'Wide (1400px)'),
        ('full', 'Full Width'),
    )
    title = models.CharField(max_length=255)
    display_type = models.CharField(max_length=10, choices=DISPLAY_CHOICES, default='carousel')
    card_size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='medium')
    container_width = models.CharField(max_length=10, choices=WIDTH_CHOICES, default='wide')
    # Dynamic filtering
    search_query = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. category=Floral&gender=men")
    max_products = models.PositiveIntegerField(default=10)
    
    # Keep ManyToMany for manual selection as optional override
    products = models.ManyToManyField('products.Product', blank=True, related_name='home_sections')
    
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.title} ({self.get_display_type_display()})"


class HomeCategory(models.Model):
    """
    Editorial category blocks.
    """
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='home/categories/')
    link = models.CharField(max_length=255)
    bottom_text = models.CharField(max_length=50, default="Shop Now")
    
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name_plural = "Home Categories"

    def __str__(self):
        return self.title


class HomeBanner(models.Model):
    """
    Singleton model for global home page settings (Fallback Hero & Promo Banner).
    """
    # Promotional Banner
    banner_big_image = models.ImageField(upload_to='home/banners/', blank=True, null=True)
    banner_small_image = models.ImageField(upload_to='home/banners/', blank=True, null=True, help_text="Mobile optimized image")
    banner_link = models.CharField(max_length=255)

    def __str__(self):
        return "Banner"

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"


class HomeReview(models.Model):
    """
    Client reviews for the homepage.
    """
    username = models.CharField(max_length=100)
    custom_job_title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    custom_image = models.ImageField(upload_to='home/reviews/', blank=True, null=True)
    
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Review by {self.username}"

    # Properties to match your HTML template exactly without needing HTML modifications
    @property
    def get_rating(self):
        return self.rating

    @property
    def get_text(self):
        return self.text

    @property
    def get_username(self):
        return self.username


class FAQSection(models.Model):
    """
    Grouping for FAQs.
    """
    title = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title


class FAQItem(models.Model):
    """
    Individual Questions and Answers.
    """
    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, related_name='items')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.question