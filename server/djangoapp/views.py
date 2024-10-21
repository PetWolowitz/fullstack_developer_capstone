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
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        # Get username and password from request body
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        # Try to check if provided credential can be authenticated
        user = authenticate(username=username, password=password)
        response_data = {"userName": username}
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            response_data["status"] = "Authenticated"
        else:
            response_data["status"] = "Failed"
            response_data["message"] = "Invalid credentials"
        return JsonResponse(response_data)
    else:
        return JsonResponse({"status": "Failed", "message": "Invalid request method"})

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"status": "Logged out"})
    else:
        return JsonResponse({"status": "Failed", "message": "Invalid request method"})

# Create a `registration` view to handle sign up request
@csrf_exempt
@csrf_exempt
@csrf_exempt
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
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
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
