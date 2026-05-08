from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from products.models import Product, ProductMedia
from .forms import ProductForm, ProductMediaFormSet
from analytics.models import PageVisit, ProductEvent

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'administration/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['total_visits'] = PageVisit.objects.count()
        context['recent_events'] = ProductEvent.objects.order_by('-created_at')[:10]
        context['recent_products'] = Product.objects.order_by('-created_at')[:5]
        return context

class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'administration/add_product.html'
    success_url = reverse_lazy('administration:dashboard')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['media_formset'] = ProductMediaFormSet(self.request.POST, self.request.FILES)
        else:
            data['media_formset'] = ProductMediaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        with transaction.atomic():
            self.object = form.save()
            if media_formset.is_valid():
                media_formset.instance = self.object
                media_formset.save()
            else:
                return self.form_invalid(form)
        messages.success(self.request, "Exquisite new fragrance added to the collection.")
        return super().form_valid(form)
