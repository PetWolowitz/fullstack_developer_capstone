from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
    path('login/', TemplateView.as_view(template_name="index.html")),  # Punto di ingresso per la pagina di login
    path('register/', TemplateView.as_view(template_name="index.html")),  # Punto di ingresso per la pagina di registrazione
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),
    path('dealers/', TemplateView.as_view(template_name="index.html")),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  