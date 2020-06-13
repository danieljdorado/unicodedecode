from django.shortcuts import render
from django.http import HttpResponse
from .forms import UnicodeTextForm
from .uni import get_normalization_form, examen_unicode


def search(request):
    """View for home page and search."""
    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            normalization_form = get_normalization_form(text)
            text = examen_unicode(text)
            return render(request, 'search.html', {'form': form,
                                                            'text': text,
                                                            'version': ud.unidata_version,
                                                            'normalization_form': normalization_form,})
    form = UnicodeTextForm()
    return render(request, 'search.html', {'form': form})


def tofu(request):
    'View for tofu page.'
    return render(request, 'tofu.html', {'title' : 'Tofu',
                                         'tagline' : 'Not just for eating'})

def about(request):
    'View function for about page of site.'
    return render(request, 'about.html', {'title' : 'About',
                                          'tagline' : 'Get to know Us'})
