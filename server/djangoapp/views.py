from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate

# Ottieni un'istanza di un logger
logger = logging.getLogger(__name__)

# Crea le tue viste qui.

# Vista per gestire la richiesta di login
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        # Ottieni username e password dal corpo della richiesta
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        # Prova ad autenticare le credenziali fornite
        user = authenticate(username=username, password=password)
        response_data = {"userName": username}
        if user is not None:
            # Se l'utente è valido, effettua il login
            login(request, user)
            response_data["status"] = "Authenticated"
        else:
            response_data["status"] = "Failed"
            response_data["message"] = "Invalid credentials"
        return JsonResponse(response_data)
    else:
        return JsonResponse({"status": "Failed", "message": "Invalid request method"})

# Vista per gestire la richiesta di logout
@csrf_exempt
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"status": "Logged out"})
    else:
        return JsonResponse({"status": "Failed", "message": "Invalid request method"})

# Vista per gestire la richiesta di registrazione
@csrf_exempt
def registration(request):
    context = {}  # Questo crea un dizionario vuoto che può essere usato più avanti
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        username_exist = False

        try:
            User.objects.get(username=username)
            username_exist = True
        except User.DoesNotExist:
            logger.debug("{} is a new user".format(username))

        if not username_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )
            login(request, user)
            context["userName"] = username
            context["status"] = "Authenticated"
            return JsonResponse(context)
        else:
            context["userName"] = username
            context["error"] = "Already Registered"
            return JsonResponse(context)
    else:
        context["status"] = "Failed"
        context["message"] = "Invalid request method"
        return JsonResponse(context)

# Vista per ottenere la lista delle auto
# views.py

def get_cars(request):
    car_model_count = CarModel.objects.count()
    print(f"CarModel count: {car_model_count}")
    if car_model_count == 0:
        initiate()
    car_models = CarModel.objects.select_related('make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.make.name,
            "DealerId": car_model.dealer_id,
            "CarType": car_model.car_type,
            "Year": car_model.year,
        })
    return JsonResponse({"CarModels": cars})
