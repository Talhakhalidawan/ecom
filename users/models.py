from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Primary user model using email as the unique identifier.
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True) # Useful for basic security/fraud checks
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email for login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

class Address(models.Model):
    """
    Separate address model allowing multiple entries (Home, Work, etc.)
    """
    ADDRESS_TYPES = (
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='shipping')
    default = models.BooleanField(default=False)
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Pakistan')

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.user.email} - {self.city} ({self.address_type})"

    def save(self, *args, **kwargs):
        """
        Logic to ensure only one default address exists per user/type.
        """
        if self.default:
            Address.objects.filter(
                user=self.user, 
                address_type=self.address_type, 
                default=True
            ).update(default=False)
        super().save(*args, **kwargs)