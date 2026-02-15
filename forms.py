from django import forms

class UnicodeTextForm(forms.Form):
    text = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'id': 'textarea1',
            'class': 'materialize-textarea',
            'dir': 'auto',
        }),
    )
    