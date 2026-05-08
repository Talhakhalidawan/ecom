import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from products.models import Product
from .models import ProductEvent

@csrf_exempt
@require_POST
def track_event(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        event_type = data.get('event_type')

        if not product_id or not event_type:
            return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

        product = Product.objects.get(id=product_id)
        
        ProductEvent.objects.create(
            product=product,
            event_type=event_type,
            session_key=request.session.session_key,
            user=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({'status': 'success'})
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
