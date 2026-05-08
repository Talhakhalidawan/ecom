from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
]
