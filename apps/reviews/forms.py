from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'content')
        labels = {
            'rating': 'Оценка',
            'content': 'Текст рецензии',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Напишите рецензию...'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None or not (1 <= rating <= 10):
            raise forms.ValidationError('Оценка должна быть от 1 до 10.')
        return rating
