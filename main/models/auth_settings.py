from django.db import models

class AuthSettings(models.Model):
    """
    Singleton model to manage login and signup page visuals and external links.
    """
    login_image = models.ImageField(
        upload_to='auth/', 
        null=True, 
        blank=True, 
        help_text="Featured image on the login page (Desktop only)."
    )
    signup_image = models.ImageField(
        upload_to='auth/', 
        null=True, 
        blank=True, 
        help_text="Featured image on the signup page (Desktop only)."
    )
    terms_link = models.CharField(
        max_length=255,
        blank=True, 
        null=True,
        help_text="Full URL to the Terms of Service page."
    )
    privacy_policy_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Full URL to the Privacy Policy page."
    )

    class Meta:
        verbose_name = "Auth Page Settings"
        verbose_name_plural = "Auth Page Settings"

    def __str__(self):
        return "Authentication Visual Settings"
