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
from django.contrib.auth.decorators import login_required
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Ottieni un'istanza di un logger
logger = logging.getLogger(__name__)

# Vista per gestire la richiesta di login
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        response_data = {"userName": username}
        if user is not None:
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
    context = {}
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

# Vista per ottenere la lista dei concessionari
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Vista per ottenere le recensioni di un concessionario
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Vista per inviare una recensione per un concessionario
@login_required
def add_review(request):
    if request.method == 'POST':
        # Controlla se l'utente è autenticato
        if not request.user.is_authenticated:
            return JsonResponse({"status": 403, "message": "Unauthorized"})

        # Estrai i dati della recensione dal corpo della richiesta
        try:
            data = json.loads(request.body)
            # Invoca la funzione post_review per inviare la recensione
            response = post_review(data)
            if response:
                return JsonResponse({"status": 200, "message": "Review added successfully"})
            else:
                return JsonResponse({"status": 500, "message": "Error in posting review"})
        except Exception as e:
            return JsonResponse({"status": 400, "message": "Bad Request", "error": str(e)})
    else:
        return JsonResponse({"status": 400, "message": "Invalid request method"})
