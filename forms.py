from django import forms

class UnicodeTextForm(forms.Form):
    text = forms.CharField(label='',widget=forms.TextInput(attrs={'id': 'textarea1', 'class': 'materialize-textarea'}))
    