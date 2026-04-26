from django import forms
from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'tags', 'is_published')
        labels = {
            'title': 'Заголовок',
            'content': 'Содержимое',
            'image': 'Изображение',
            'tags': 'Теги',
            'is_published': 'Опубликовать',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Текст поста...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'тег1, тег2, тег3'}),
        }


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
