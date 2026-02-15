from django.urls import path
from unicodedecode import views

urlpatterns = [
    path('', views.decode, name='decode'),
    path('about', views.about, name='about'),
    path('codepoint/<slug:slug>', views.codepoint, name='codepoint'),
    path('terms', views.terms, name='terms'),
    path('tofu', views.tofu, name='tofu'),
    path('privacy', views.privacy, name='privacy'),
]
