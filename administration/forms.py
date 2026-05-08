from django import forms
from products.models import Product, ProductMedia, Size

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'short_description', 'description', 'category',
            'gender', 'concentration', 'sizes', 'base_price', 'sale_price',
            'stock_quantity', 'is_bestseller', 'is_new_arrival',
            'top_notes', 'heart_notes', 'base_notes',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
            'sizes': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full bg-gray-50 border border-gray-100 px-4 py-3 text-sm focus:outline-none focus:border-black transition-all'
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                 field.widget.attrs['class'] = 'flex flex-wrap gap-4 text-sm'
            if isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs['class'] = 'w-5 h-5 accent-black'

class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ['file', 'alt_text', 'is_main', 'display_order']

ProductMediaFormSet = forms.inlineformset_factory(
    Product, ProductMedia, form=ProductMediaForm,
    extra=5, can_delete=True
)
