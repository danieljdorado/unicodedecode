from django.shortcuts import render
from django.http import HttpResponse
from .forms import UnicodeTextForm
from .uni import get_normalization_form, examen_unicode


def search(request):
    """Home and search."""
    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            normalization_form = get_normalization_form(text)
            text = examen_unicode(text)
            return render(request, 'search.html', {'form': form,
                                                    'text': text,
                                                    'normalization_form': normalization_form,
                                                    'title' : 'Unicode Search',
                                                    'tagline' : 'Examine a Unicode String'})
    form = UnicodeTextForm()
    return render(request, 'home.html', {'form': form})


def tofu(request):
    """Tofu page."""
    return render(request, 'tofu.html', {'title' : 'Tofu',
                                         'tagline' : 'Not Just For Eating'})
