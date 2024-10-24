from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('get_cars/', views.get_cars, name='get_cars'),
    # path for dealer reviews view
<<<<<<< HEAD
   path('get_dealers/', views.get_dealerships, name='get_dealers'),
=======
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
>>>>>>> d23f545bd2cecb6a484be2a98633b59c4d404b54
    path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    # Route per ottenere le recensioni di un concessionario specifico
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
