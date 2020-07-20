from django.urls import path
from decode import views

urlpatterns = [
    path('', views.decode, name='decode'),
    path('about', views.about, name='about'),
    path('character/<slug:slug>', views.character, name='character'),
    path('terms', views.terms, name='terms'),
    path('tofu', views.tofu, name='tofu'),
    path('privacy', views.privacy, name='privacy'),
]
