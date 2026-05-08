from .models import PageVisit

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # We only track successful GET requests for non-static/media/admin paths
        if request.method == 'GET' and response.status_code == 200:
            path = request.path
            
            # Exclude noise
            exclusions = ['/static/', '/media/', '/admin/', '/__browser_reload__/']
            if not any(path.startswith(ex) for ex in exclusions):
                try:
                    PageVisit.objects.create(
                        path=path,
                        referrer=request.META.get('HTTP_REFERER', ''),
                        session_key=request.session.session_key,
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                except Exception:
                    # Fail silently to not break the user experience
                    pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
