from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'hidden', 'id': 'form-rating'}),
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-gray-200 px-5 py-4 focus:outline-none focus:border-theme_primary font-sans text-sm placeholder:text-gray-400',
                'placeholder': 'Review Title'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full bg-white border border-gray-200 px-5 py-4 focus:outline-none focus:border-theme_primary font-sans text-sm placeholder:text-gray-400 min-h-[150px]',
                'placeholder': 'Your Review Content',
                'rows': 5
            }),
        }
