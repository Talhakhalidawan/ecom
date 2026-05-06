from main.models import AuthSettings

def auth_settings_context(request):
    """
    Injects authentication-related settings into the context.
    """
    return {
        'auth_settings': AuthSettings.objects.first()
    }
