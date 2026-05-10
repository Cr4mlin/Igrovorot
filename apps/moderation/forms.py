from django import forms
from moderation.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('reason',)
        labels = {'reason': 'Причина жалобы'}
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Опишите нарушение...'}),
        }
