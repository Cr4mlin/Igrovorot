from django import forms
from posts.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Написать комментарий...',
            }),
        }
