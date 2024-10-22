import requests
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# URL del backend e del sentiment analyzer estratte dal file .env
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# Funzione per fare una richiesta GET al backend
def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"
    
    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))
    
    try:
        # Esegui la richiesta GET usando la libreria requests
        response = requests.get(request_url)
        # Verifica se la richiesta ha avuto successo (status code 200)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return None
    except Exception as e:
        # Gestione degli errori di rete
        print(f"Network exception occurred: {e}")
        return None

# Funzione per analizzare i sentimenti delle recensioni
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    print(f"GET from {request_url}")
    try:
        # Esegui la richiesta GET usando la libreria requests
        response = requests.get(request_url)
        # Verifica se la richiesta ha avuto successo
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Errore nella richiesta: {response.status_code}")
            return None
    except Exception as err:
        # Gestione degli errori di rete
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

# Funzione per inviare una recensione tramite una richiesta POST
def post_review(data_dict):
    request_url = backend_url + "add_review"
    try:
        # Esegui la richiesta POST usando la libreria requests
        response = requests.post(request_url, json=data_dict)
        # Verifica se la richiesta ha avuto successo
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Errore nella richiesta POST: {response.status_code}")
            return None
    except Exception as err:
        # Gestione degli errori di rete
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

#Funzione per inviare la recensione al backend
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None