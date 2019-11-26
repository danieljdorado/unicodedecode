from django import forms

class UnicodeTextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 50, 'cols':50}))