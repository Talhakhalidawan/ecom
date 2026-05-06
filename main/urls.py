from django.urls import path
from .views import home, static_page_detail

urlpatterns = [
    path('', home, name='home'),
    path('pages/<slug:slug>/', static_page_detail, name='static_page_detail'),
]
