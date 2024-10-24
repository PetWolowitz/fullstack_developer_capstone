from django.urls import path, include  # Aggiungi include qui
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import post_review

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('get_cars/', views.get_cars, name='get_cars'),
    # path for dealer reviews view
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    # Route per ottenere le recensioni di un concessionario specifico
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_details'),
    path('add_review/<int:dealer_id>/', views.post_review, name='post_review'),
    path('djangoapp/dealer/<int:dealer_id>/', views.get_dealer_detail, name='get_dealer_details')

    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
